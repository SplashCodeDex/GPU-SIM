"""
Surround Configuration Panel
Shows multi-monitor Surround setup similar to real NVIDIA Control Panel.
"""

from typing import Optional
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox,
    QComboBox, QPushButton, QFrame, QGridLayout, QCheckBox,
    QSpinBox
)
from PyQt5.QtGui import QFont, QPainter, QColor, QBrush, QPen
from PyQt5.QtCore import Qt, QRect

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.gpu_profile import GPUProfile


class MonitorPreview(QFrame):
    """Visual preview of monitor arrangement."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(150)
        self.setStyleSheet("background-color: #1a1a1a; border: 1px solid #404040; border-radius: 5px;")
        self._monitors = 1
        self._surround_enabled = False

    def set_monitors(self, count: int, surround: bool = False) -> None:
        self._monitors = count
        self._surround_enabled = surround
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Calculate monitor positions
        total_width = self.width() - 40
        total_height = self.height() - 40

        if self._surround_enabled and self._monitors > 1:
            # Surround mode - monitors side by side
            monitor_width = total_width // self._monitors - 10
            monitor_height = int(monitor_width * 9 / 16)

            for i in range(self._monitors):
                x = 20 + i * (monitor_width + 10)
                y = (self.height() - monitor_height) // 2

                # Monitor frame
                painter.setPen(QPen(QColor("#76B900"), 2))
                painter.setBrush(QBrush(QColor("#2d2d2d")))
                painter.drawRect(x, y, monitor_width, monitor_height)

                # Monitor number
                painter.setPen(QColor("white"))
                painter.drawText(QRect(x, y, monitor_width, monitor_height),
                               Qt.AlignCenter, str(i + 1))
        else:
            # Single monitor mode
            monitor_width = min(200, total_width)
            monitor_height = int(monitor_width * 9 / 16)
            x = (self.width() - monitor_width) // 2
            y = (self.height() - monitor_height) // 2

            painter.setPen(QPen(QColor("#76B900"), 2))
            painter.setBrush(QBrush(QColor("#2d2d2d")))
            painter.drawRect(x, y, monitor_width, monitor_height)

            painter.setPen(QColor("white"))
            painter.drawText(QRect(x, y, monitor_width, monitor_height),
                           Qt.AlignCenter, "Primary Display")


class SurroundPanel(QWidget):
    """
    NVIDIA Surround Configuration panel.
    Shows multi-monitor setup options.
    """

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._profile: Optional[GPUProfile] = None
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the panel UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header
        header = QLabel("Configure Surround, PhysX")
        header.setFont(QFont("Segoe UI", 16, QFont.Bold))
        layout.addWidget(header)

        desc = QLabel(
            "Configure NVIDIA Surround to span your desktop across multiple displays "
            "for an immersive gaming experience."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #888;")
        layout.addWidget(desc)

        # Monitor preview
        self._preview = MonitorPreview()
        layout.addWidget(self._preview)

        # Surround configuration
        surround_group = QGroupBox("Surround configuration")
        surround_layout = QVBoxLayout(surround_group)

        self._enable_surround = QCheckBox("Span displays with Surround")
        self._enable_surround.stateChanged.connect(self._on_surround_changed)
        surround_layout.addWidget(self._enable_surround)

        # Monitor count
        monitors_layout = QHBoxLayout()
        monitors_layout.addWidget(QLabel("Number of displays:"))
        self._monitor_count = QSpinBox()
        self._monitor_count.setRange(1, 5)
        self._monitor_count.setValue(1)
        self._monitor_count.valueChanged.connect(self._update_preview)
        monitors_layout.addWidget(self._monitor_count)
        monitors_layout.addStretch()
        surround_layout.addLayout(monitors_layout)

        # Resolution
        res_layout = QHBoxLayout()
        res_layout.addWidget(QLabel("Surround resolution:"))
        self._resolution_combo = QComboBox()
        self._resolution_combo.addItems([
            "5760 x 1080 (3 x 1920x1080)",
            "7680 x 1440 (3 x 2560x1440)",
            "11520 x 2160 (3 x 3840x2160)",
        ])
        res_layout.addWidget(self._resolution_combo)
        res_layout.addStretch()
        surround_layout.addLayout(res_layout)

        layout.addWidget(surround_group)

        # Bezel correction
        bezel_group = QGroupBox("Bezel correction")
        bezel_layout = QHBoxLayout(bezel_group)

        bezel_layout.addWidget(QLabel("Horizontal overlap:"))
        self._bezel_spin = QSpinBox()
        self._bezel_spin.setRange(0, 200)
        self._bezel_spin.setValue(0)
        self._bezel_spin.setSuffix(" pixels")
        bezel_layout.addWidget(self._bezel_spin)
        bezel_layout.addStretch()

        layout.addWidget(bezel_group)

        # Apply button
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        apply_btn = QPushButton("Apply")
        apply_btn.setStyleSheet("background-color: #76B900; color: white; padding: 8px 20px;")
        btn_layout.addWidget(apply_btn)

        layout.addLayout(btn_layout)
        layout.addStretch()

    def _on_surround_changed(self, state: int) -> None:
        self._update_preview()

    def _update_preview(self) -> None:
        self._preview.set_monitors(
            self._monitor_count.value(),
            self._enable_surround.isChecked()
        )

    def set_profile(self, profile: Optional[GPUProfile]) -> None:
        """Set the GPU profile."""
        self._profile = profile
