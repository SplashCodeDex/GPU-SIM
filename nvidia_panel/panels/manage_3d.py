"""
Manage 3D Settings Panel
Shows 3D graphics settings similar to real NVIDIA Control Panel.
"""

from typing import Optional
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox,
    QFormLayout, QComboBox, QSlider, QCheckBox, QScrollArea,
    QFrame, QPushButton, QTabWidget
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.gpu_profile import GPUProfile


class Manage3DPanel(QWidget):
    """
    3D Settings management panel.
    Shows graphics settings with sliders and dropdowns.
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
        header = QLabel("Manage 3D settings")
        header.setFont(QFont("Segoe UI", 16, QFont.Bold))
        layout.addWidget(header)

        desc = QLabel("Customize your 3D settings for all programs or specific programs.")
        desc.setStyleSheet("color: #888;")
        layout.addWidget(desc)

        # Tabs
        tabs = QTabWidget()
        tabs.addTab(self._create_global_settings(), "Global Settings")
        tabs.addTab(self._create_program_settings(), "Program Settings")
        layout.addWidget(tabs)

        # Apply/Reset buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        restore_btn = QPushButton("Restore Defaults")
        btn_layout.addWidget(restore_btn)

        apply_btn = QPushButton("Apply")
        apply_btn.setStyleSheet("background-color: #76B900; color: white;")
        btn_layout.addWidget(apply_btn)

        layout.addLayout(btn_layout)

    def _create_global_settings(self) -> QWidget:
        """Create global settings tab."""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(15)

        # Image Sharpening
        sharpen_group = QGroupBox("Image Sharpening")
        sharpen_layout = QFormLayout(sharpen_group)

        sharpen_combo = QComboBox()
        sharpen_combo.addItems(["Off", "On", "GPU Scaling"])
        sharpen_layout.addRow("Sharpening:", sharpen_combo)

        layout.addWidget(sharpen_group)

        # Antialiasing
        aa_group = QGroupBox("Antialiasing")
        aa_layout = QFormLayout(aa_group)

        aa_mode = QComboBox()
        aa_mode.addItems(["Application-controlled", "Off", "Override"])
        aa_layout.addRow("Mode:", aa_mode)

        aa_setting = QComboBox()
        aa_setting.addItems(["None", "2x", "4x", "8x", "16x"])
        aa_setting.setCurrentText("4x")
        aa_layout.addRow("Setting:", aa_setting)

        aa_fxaa = QCheckBox("FXAA")
        aa_layout.addRow("", aa_fxaa)

        layout.addWidget(aa_group)

        # Texture Filtering
        tf_group = QGroupBox("Texture Filtering")
        tf_layout = QFormLayout(tf_group)

        tf_quality = QComboBox()
        tf_quality.addItems(["High performance", "Performance", "Quality", "High quality"])
        tf_quality.setCurrentText("Quality")
        tf_layout.addRow("Quality:", tf_quality)

        tf_aniso = QComboBox()
        tf_aniso.addItems(["Application-controlled", "Off", "2x", "4x", "8x", "16x"])
        tf_aniso.setCurrentText("16x")
        tf_layout.addRow("Anisotropic filtering:", tf_aniso)

        layout.addWidget(tf_group)

        # Power Management
        power_group = QGroupBox("Power management mode")
        power_layout = QFormLayout(power_group)

        power_mode = QComboBox()
        power_mode.addItems(["Optimal power", "Adaptive", "Prefer maximum performance"])
        power_mode.setCurrentText("Prefer maximum performance")
        power_layout.addRow("Mode:", power_mode)

        layout.addWidget(power_group)

        # Vertical Sync
        vsync_group = QGroupBox("Vertical sync")
        vsync_layout = QFormLayout(vsync_group)

        vsync = QComboBox()
        vsync.addItems(["Use the 3D application setting", "Off", "On", "Fast", "Adaptive"])
        vsync_layout.addRow("Setting:", vsync)

        layout.addWidget(vsync_group)

        # Low Latency Mode
        latency_group = QGroupBox("Low Latency Mode")
        latency_layout = QFormLayout(latency_group)

        latency = QComboBox()
        latency.addItems(["Off", "On", "Ultra"])
        latency.setCurrentText("On")
        latency_layout.addRow("Mode:", latency)

        layout.addWidget(latency_group)

        layout.addStretch()
        scroll.setWidget(content)
        return scroll

    def _create_program_settings(self) -> QWidget:
        """Create program settings tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)

        # Program selector
        select_layout = QHBoxLayout()
        select_layout.addWidget(QLabel("Select a program to customize:"))

        program_combo = QComboBox()
        program_combo.addItems([
            "Global",
            "3DMark",
            "Adobe Premiere Pro",
            "Cyberpunk 2077",
            "DaVinci Resolve",
            "Fortnite",
            "Microsoft Flight Simulator",
            "Valorant"
        ])
        select_layout.addWidget(program_combo)
        select_layout.addStretch()

        layout.addLayout(select_layout)

        # Info label
        info = QLabel("Program-specific settings override global settings for the selected program.")
        info.setStyleSheet("color: #888;")
        layout.addWidget(info)

        layout.addStretch()
        return widget

    def set_profile(self, profile: Optional[GPUProfile]) -> None:
        """Set the GPU profile."""
        self._profile = profile
