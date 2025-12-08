"""
Metrics Dashboard Panel
Live GPU metrics display with animated graphs and gauges.
"""

from typing import Optional, List, Deque
from collections import deque
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox,
    QProgressBar, QGridLayout, QSlider, QPushButton, QFrame
)
from PyQt5.QtGui import QFont, QPainter, QColor, QPen, QBrush, QPainterPath
from PyQt5.QtCore import Qt, QTimer, QRectF, pyqtSignal

import sys
sys.path.insert(0, str(__file__).rsplit('src', 1)[0])

from src.core.gpu_profile import GPUProfile
from src.metrics.gpu_metrics import get_metrics_generator, GPUMetrics


class MetricGauge(QWidget):
    """Circular gauge widget for displaying a single metric."""

    def __init__(self, title: str, unit: str = "%",
                 min_val: float = 0, max_val: float = 100,
                 warning_threshold: float = 70, danger_threshold: float = 90,
                 parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.title = title
        self.unit = unit
        self.min_val = min_val
        self.max_val = max_val
        self.warning = warning_threshold
        self.danger = danger_threshold
        self.value = 0.0

        self.setMinimumSize(120, 120)
        self.setMaximumSize(150, 150)

    def set_value(self, value: float) -> None:
        self.value = max(self.min_val, min(self.max_val, value))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        size = min(w, h) - 10

        # Center the gauge
        x = (w - size) / 2
        y = (h - size) / 2
        rect = QRectF(x, y, size, size)

        # Background arc
        painter.setPen(QPen(QColor(60, 60, 60), 10, Qt.SolidLine, Qt.RoundCap))
        painter.drawArc(rect, 225 * 16, -270 * 16)

        # Value arc
        percent = (self.value - self.min_val) / (self.max_val - self.min_val)
        angle = int(-270 * percent * 16)

        # Color based on value
        if self.value >= self.danger:
            color = QColor(220, 50, 50)  # Red
        elif self.value >= self.warning:
            color = QColor(255, 180, 0)  # Yellow
        else:
            color = QColor(118, 185, 0)  # NVIDIA Green

        painter.setPen(QPen(color, 10, Qt.SolidLine, Qt.RoundCap))
        painter.drawArc(rect, 225 * 16, angle)

        # Center text
        painter.setPen(QColor(200, 200, 200))
        painter.setFont(QFont("Segoe UI", 16, QFont.Bold))

        if self.value >= 10:
            value_text = f"{self.value:.0f}"
        else:
            value_text = f"{self.value:.1f}"

        painter.drawText(rect, Qt.AlignCenter, value_text + self.unit)

        # Title below
        painter.setFont(QFont("Segoe UI", 9))
        painter.setPen(QColor(150, 150, 150))
        title_rect = QRectF(x, y + size - 15, size, 20)
        painter.drawText(title_rect, Qt.AlignCenter, self.title)


class LineGraph(QWidget):
    """Scrolling line graph for time-series data."""

    def __init__(self, title: str, color: QColor = QColor(118, 185, 0),
                 max_points: int = 60, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.title = title
        self.color = color
        self.max_points = max_points
        self.data: Deque[float] = deque(maxlen=max_points)
        self.max_val = 100.0

        self.setMinimumHeight(80)
        self.setMaximumHeight(100)

        # Initialize with zeros
        for _ in range(max_points):
            self.data.append(0)

    def add_value(self, value: float) -> None:
        self.data.append(value)
        self.update()

    def set_max(self, max_val: float) -> None:
        self.max_val = max_val

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height() - 20  # Leave space for title
        margin = 5

        # Background
        painter.fillRect(0, 0, w, self.height(), QColor(30, 30, 30))

        # Grid lines
        painter.setPen(QPen(QColor(50, 50, 50), 1))
        for i in range(5):
            y = margin + (h * i / 4)
            painter.drawLine(margin, int(y), w - margin, int(y))

        # Draw line graph
        if len(self.data) > 1:
            path = QPainterPath()

            step = (w - 2 * margin) / (len(self.data) - 1)

            for i, value in enumerate(self.data):
                x = margin + i * step
                y = margin + h - (value / self.max_val * h)

                if i == 0:
                    path.moveTo(x, y)
                else:
                    path.lineTo(x, y)

            # Draw fill
            fill_path = QPainterPath(path)
            fill_path.lineTo(margin + (len(self.data) - 1) * step, margin + h)
            fill_path.lineTo(margin, margin + h)
            fill_path.closeSubpath()

            painter.fillPath(fill_path, QBrush(QColor(self.color.red(),
                                                       self.color.green(),
                                                       self.color.blue(), 50)))

            # Draw line
            painter.setPen(QPen(self.color, 2))
            painter.drawPath(path)

        # Current value
        if self.data:
            painter.setPen(QColor(200, 200, 200))
            painter.setFont(QFont("Segoe UI", 10, QFont.Bold))
            value_text = f"{self.data[-1]:.1f}%"
            painter.drawText(w - 60, 20, value_text)

        # Title
        painter.setFont(QFont("Segoe UI", 9))
        painter.setPen(QColor(120, 120, 120))
        painter.drawText(margin, self.height() - 5, self.title)


class MetricsDashboardPanel(QWidget):
    """
    Enhanced dashboard with live fake GPU metrics.
    """

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._current_profile: Optional[GPUProfile] = None
        self._metrics_generator = get_metrics_generator()

        self._setup_ui()
        self._setup_timer()

    def _setup_ui(self) -> None:
        """Set up the panel UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header
        header_layout = QHBoxLayout()

        title = QLabel("📊 Live GPU Metrics")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        header_layout.addWidget(title)

        header_layout.addStretch()

        # Status indicator
        self._status_label = QLabel("● SIMULATING")
        self._status_label.setStyleSheet("color: #76b900; font-weight: bold;")
        header_layout.addWidget(self._status_label)

        layout.addLayout(header_layout)

        # Gauges row
        gauges_layout = QHBoxLayout()

        self._gpu_gauge = MetricGauge("GPU", "%")
        gauges_layout.addWidget(self._gpu_gauge)

        self._mem_gauge = MetricGauge("Memory", "%")
        gauges_layout.addWidget(self._mem_gauge)

        self._temp_gauge = MetricGauge("Temp", "°C", 0, 100, 70, 85)
        gauges_layout.addWidget(self._temp_gauge)

        self._power_gauge = MetricGauge("Power", "W", 0, 350, 250, 320)
        gauges_layout.addWidget(self._power_gauge)

        self._fan_gauge = MetricGauge("Fan", "%", 0, 100)
        gauges_layout.addWidget(self._fan_gauge)

        layout.addLayout(gauges_layout)

        # Graphs
        graphs_group = QGroupBox("Activity")
        graphs_layout = QVBoxLayout(graphs_group)

        self._gpu_graph = LineGraph("GPU Utilization", QColor(118, 185, 0))
        graphs_layout.addWidget(self._gpu_graph)

        self._mem_graph = LineGraph("Memory Usage", QColor(0, 150, 255))
        graphs_layout.addWidget(self._mem_graph)

        layout.addWidget(graphs_group)

        # Details grid
        details_group = QGroupBox("Details")
        details_layout = QGridLayout(details_group)

        labels = [
            ("GPU Clock:", "gpu_clock"),
            ("Memory Clock:", "mem_clock"),
            ("Memory Used:", "mem_used"),
            ("Power Draw:", "power_draw"),
        ]

        self._detail_labels = {}
        for i, (title, key) in enumerate(labels):
            row = i // 2
            col = (i % 2) * 2

            title_label = QLabel(title)
            title_label.setStyleSheet("color: #888;")
            details_layout.addWidget(title_label, row, col)

            value_label = QLabel("--")
            value_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
            self._detail_labels[key] = value_label
            details_layout.addWidget(value_label, row, col + 1)

        layout.addWidget(details_group)

        # Load simulation controls
        controls_group = QGroupBox("Load Simulation")
        controls_layout = QHBoxLayout(controls_group)

        controls_layout.addWidget(QLabel("Simulated Load:"))

        self._load_slider = QSlider(Qt.Horizontal)
        self._load_slider.setRange(0, 100)
        self._load_slider.setValue(0)
        self._load_slider.valueChanged.connect(self._on_load_changed)
        controls_layout.addWidget(self._load_slider)

        self._load_label = QLabel("0%")
        self._load_label.setMinimumWidth(40)
        controls_layout.addWidget(self._load_label)

        # Preset buttons
        presets = [("Idle", 5), ("Light", 25), ("Medium", 50), ("Heavy", 80), ("Max", 100)]
        for name, value in presets:
            btn = QPushButton(name)
            btn.setMaximumWidth(60)
            btn.clicked.connect(lambda checked, v=value: self._load_slider.setValue(v))
            controls_layout.addWidget(btn)

        layout.addWidget(controls_group)

        layout.addStretch()

    def _setup_timer(self) -> None:
        """Set up update timer."""
        self._timer = QTimer()
        self._timer.timeout.connect(self._update_metrics)
        self._timer.start(100)  # 10 FPS

    def _on_load_changed(self, value: int) -> None:
        """Handle load slider change."""
        self._load_label.setText(f"{value}%")
        self._metrics_generator.set_load(value)

    def _update_metrics(self) -> None:
        """Update displayed metrics."""
        m = self._metrics_generator.current_metrics

        # Update gauges
        self._gpu_gauge.set_value(m.gpu_utilization)
        self._mem_gauge.set_value(m.memory_utilization)
        self._temp_gauge.set_value(m.temperature_core)
        self._power_gauge.set_value(m.power_draw_watts)
        self._fan_gauge.set_value(m.fan_speed_percent)

        # Update graphs
        self._gpu_graph.add_value(m.gpu_utilization)
        self._mem_graph.add_value(m.memory_utilization)

        # Update details
        self._detail_labels["gpu_clock"].setText(f"{m.gpu_clock_mhz} MHz")
        self._detail_labels["mem_clock"].setText(f"{m.memory_clock_mhz} MHz")
        self._detail_labels["mem_used"].setText(
            f"{m.memory_used_mb:,.0f} / {m.memory_total_mb:,.0f} MB"
        )
        self._detail_labels["power_draw"].setText(
            f"{m.power_draw_watts:.0f} / {m.power_limit_watts:.0f} W"
        )

    def set_profile(self, profile: Optional[GPUProfile]) -> None:
        """Update panel with a GPU profile."""
        self._current_profile = profile
        self._metrics_generator.set_profile(profile)

        if profile:
            self._metrics_generator.start()
            self._power_gauge.max_val = profile.tdp_watts
            self._power_gauge.warning = profile.tdp_watts * 0.85
            self._power_gauge.danger = profile.tdp_watts * 0.95
            self._status_label.setText(f"● {profile.name}")
        else:
            self._metrics_generator.stop()
            self._status_label.setText("● NO GPU SELECTED")
            self._status_label.setStyleSheet("color: #666;")

    def showEvent(self, event):
        super().showEvent(event)
        if self._current_profile:
            self._metrics_generator.start()

    def hideEvent(self, event):
        super().hideEvent(event)
        # Don't stop metrics - might be used elsewhere
