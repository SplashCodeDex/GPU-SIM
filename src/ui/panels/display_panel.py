"""
Display Panel
Panel for display settings configuration (resolution, refresh rate, rotation).
"""

from typing import Optional
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox,
    QComboBox, QSlider, QPushButton, QCheckBox, QSpinBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

import sys
sys.path.insert(0, str(__file__).rsplit('src', 1)[0])

from src.core.gpu_profile import GPUProfile


class DisplayPanel(QWidget):
    """
    Panel for display and resolution settings.
    Simulates NVIDIA Control Panel display configuration.
    """

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._current_profile: Optional[GPUProfile] = None
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the panel UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Header
        header = QLabel("Display Settings")
        header.setFont(QFont("Segoe UI", 18, QFont.Bold))
        layout.addWidget(header)

        subtitle = QLabel("Configure display resolution and refresh rate")
        subtitle.setStyleSheet("color: #888;")
        layout.addWidget(subtitle)

        # Resolution Group
        resolution_group = QGroupBox("Resolution")
        resolution_layout = QVBoxLayout(resolution_group)

        res_row = QHBoxLayout()
        res_row.addWidget(QLabel("Resolution:"))
        self._resolution_combo = QComboBox()
        self._resolution_combo.addItems([
            "3840 x 2160 (4K UHD)",
            "2560 x 1440 (QHD)",
            "1920 x 1080 (Full HD)",
            "1680 x 1050",
            "1600 x 900",
            "1366 x 768",
            "1280 x 720 (HD)",
        ])
        self._resolution_combo.setCurrentIndex(2)  # Default to 1080p
        res_row.addWidget(self._resolution_combo)
        res_row.addStretch()
        resolution_layout.addLayout(res_row)

        refresh_row = QHBoxLayout()
        refresh_row.addWidget(QLabel("Refresh Rate:"))
        self._refresh_combo = QComboBox()
        self._refresh_combo.addItems([
            "144 Hz",
            "120 Hz",
            "75 Hz",
            "60 Hz",
            "50 Hz",
            "30 Hz",
        ])
        self._refresh_combo.setCurrentIndex(3)  # Default to 60Hz
        refresh_row.addWidget(self._refresh_combo)
        refresh_row.addStretch()
        resolution_layout.addLayout(refresh_row)

        layout.addWidget(resolution_group)

        # Color Settings Group
        color_group = QGroupBox("Color Settings")
        color_layout = QVBoxLayout(color_group)

        depth_row = QHBoxLayout()
        depth_row.addWidget(QLabel("Color Depth:"))
        self._depth_combo = QComboBox()
        self._depth_combo.addItems([
            "32-bit (True Color)",
            "16-bit (High Color)",
            "8-bit",
        ])
        depth_row.addWidget(self._depth_combo)
        depth_row.addStretch()
        color_layout.addLayout(depth_row)

        output_row = QHBoxLayout()
        output_row.addWidget(QLabel("Output Color Format:"))
        self._output_combo = QComboBox()
        self._output_combo.addItems([
            "RGB",
            "YCbCr444",
            "YCbCr422",
        ])
        output_row.addWidget(self._output_combo)
        output_row.addStretch()
        color_layout.addLayout(output_row)

        dynamic_range_row = QHBoxLayout()
        dynamic_range_row.addWidget(QLabel("Output Dynamic Range:"))
        self._dynamic_combo = QComboBox()
        self._dynamic_combo.addItems(["Full", "Limited"])
        dynamic_range_row.addWidget(self._dynamic_combo)
        dynamic_range_row.addStretch()
        color_layout.addLayout(dynamic_range_row)

        layout.addWidget(color_group)

        # Rotation Group
        rotation_group = QGroupBox("Display Rotation")
        rotation_layout = QVBoxLayout(rotation_group)

        rot_row = QHBoxLayout()
        rot_row.addWidget(QLabel("Orientation:"))
        self._rotation_combo = QComboBox()
        self._rotation_combo.addItems([
            "Landscape",
            "Portrait",
            "Landscape (flipped)",
            "Portrait (flipped)",
        ])
        rot_row.addWidget(self._rotation_combo)
        rot_row.addStretch()
        rotation_layout.addLayout(rot_row)

        layout.addWidget(rotation_group)

        # Scaling Group
        scaling_group = QGroupBox("Scaling")
        scaling_layout = QVBoxLayout(scaling_group)

        scaling_row = QHBoxLayout()
        scaling_row.addWidget(QLabel("Scaling Mode:"))
        self._scaling_combo = QComboBox()
        self._scaling_combo.addItems([
            "No scaling",
            "Aspect ratio",
            "Full-screen",
            "Integer scaling",
        ])
        self._scaling_combo.setCurrentIndex(1)
        scaling_row.addWidget(self._scaling_combo)
        scaling_row.addStretch()
        scaling_layout.addLayout(scaling_row)

        self._gpu_scaling_check = QCheckBox("Perform scaling on GPU")
        self._gpu_scaling_check.setChecked(True)
        scaling_layout.addWidget(self._gpu_scaling_check)

        layout.addWidget(scaling_group)

        # Buttons
        btn_layout = QHBoxLayout()

        self._detect_btn = QPushButton("Detect Displays")
        btn_layout.addWidget(self._detect_btn)

        self._identify_btn = QPushButton("Identify")
        btn_layout.addWidget(self._identify_btn)

        btn_layout.addStretch()

        self._apply_btn = QPushButton("Apply")
        self._apply_btn.setStyleSheet("""
            QPushButton {
                background-color: #76b900;
                color: white;
                border: none;
                padding: 8px 20px;
            }
        """)
        btn_layout.addWidget(self._apply_btn)

        layout.addLayout(btn_layout)
        layout.addStretch()

        # Note
        note = QLabel("Note: These settings are simulated for demonstration purposes")
        note.setStyleSheet("color: #666; font-size: 11px;")
        layout.addWidget(note)

    def set_profile(self, profile: Optional[GPUProfile]) -> None:
        """Update panel based on selected profile."""
        self._current_profile = profile

        if profile and profile.display_modes:
            # Update resolution combo with profile's supported modes
            self._resolution_combo.clear()
            for mode in profile.display_modes:
                self._resolution_combo.addItem(
                    f"{mode.width} x {mode.height} @ {mode.refresh}Hz"
                )

        self.setEnabled(profile is not None)
