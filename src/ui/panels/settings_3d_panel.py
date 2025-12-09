"""
Settings 3D Panel
Panel for configuring 3D settings (simulated).
"""

from typing import Optional
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox,
    QSlider, QComboBox, QCheckBox, QSpinBox, QPushButton
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

import sys
sys.path.insert(0, str(__file__).rsplit('src', 1)[0])

from src.core.gpu_profile import GPUProfile


class Settings3DPanel(QWidget):
    """
    Panel for simulated 3D graphics settings.
    These are cosmetic UI elements that mimic NVIDIA Control Panel.
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
        header = QLabel("Manage 3D Settings")
        header.setFont(QFont("Segoe UI", 18, QFont.Bold))
        layout.addWidget(header)

        subtitle = QLabel("Configure global 3D settings for applications")
        subtitle.setStyleSheet("color: #888;")
        layout.addWidget(subtitle)

        # Global Settings
        global_group = QGroupBox("Global Presets")
        global_layout = QVBoxLayout(global_group)

        preset_layout = QHBoxLayout()
        preset_layout.addWidget(QLabel("Performance Preset:"))

        self._preset_combo = QComboBox()
        self._preset_combo.addItems([
            "Let the application decide",
            "Performance",
            "Quality",
            "High Quality",
            "Custom"
        ])
        self._preset_combo.setCurrentIndex(0)
        preset_layout.addWidget(self._preset_combo)
        preset_layout.addStretch()

        global_layout.addLayout(preset_layout)
        layout.addWidget(global_group)

        # Image Quality
        quality_group = QGroupBox("Image Quality")
        quality_layout = QVBoxLayout(quality_group)

        # Anti-aliasing
        aa_layout = QHBoxLayout()
        aa_layout.addWidget(QLabel("Anti-aliasing Mode:"))
        self._aa_combo = QComboBox()
        self._aa_combo.addItems(["Off", "FXAA", "2x MSAA", "4x MSAA", "8x MSAA"])
        self._aa_combo.setCurrentIndex(1)
        aa_layout.addWidget(self._aa_combo)
        aa_layout.addStretch()
        quality_layout.addLayout(aa_layout)

        # Texture Filtering
        tf_layout = QHBoxLayout()
        tf_layout.addWidget(QLabel("Texture Filtering Quality:"))
        self._tf_combo = QComboBox()
        self._tf_combo.addItems(["High Performance", "Performance", "Quality", "High Quality"])
        self._tf_combo.setCurrentIndex(2)
        tf_layout.addWidget(self._tf_combo)
        tf_layout.addStretch()
        quality_layout.addLayout(tf_layout)

        # Anisotropic Filtering
        af_layout = QHBoxLayout()
        af_layout.addWidget(QLabel("Anisotropic Filtering:"))
        self._af_combo = QComboBox()
        self._af_combo.addItems(["Off", "2x", "4x", "8x", "16x"])
        self._af_combo.setCurrentIndex(4)
        af_layout.addWidget(self._af_combo)
        af_layout.addStretch()
        quality_layout.addLayout(af_layout)

        layout.addWidget(quality_group)

        # Performance Settings
        perf_group = QGroupBox("Performance")
        perf_layout = QVBoxLayout(perf_group)

        # VSync
        vsync_layout = QHBoxLayout()
        self._vsync_check = QCheckBox("Vertical Sync (V-Sync)")
        self._vsync_check.setChecked(True)
        vsync_layout.addWidget(self._vsync_check)
        perf_layout.addLayout(vsync_layout)

        # Triple Buffering
        triple_layout = QHBoxLayout()
        self._triple_check = QCheckBox("Triple Buffering")
        triple_layout.addWidget(self._triple_check)
        perf_layout.addLayout(triple_layout)

        # Max Frame Rate
        fps_layout = QHBoxLayout()
        fps_layout.addWidget(QLabel("Max Frame Rate:"))
        self._fps_spin = QSpinBox()
        self._fps_spin.setRange(0, 500)
        self._fps_spin.setValue(0)
        self._fps_spin.setSpecialValueText("Unlimited")
        fps_layout.addWidget(self._fps_spin)
        fps_layout.addStretch()
        perf_layout.addLayout(fps_layout)

        # Power Management
        power_layout = QHBoxLayout()
        power_layout.addWidget(QLabel("Power Management Mode:"))
        self._power_combo = QComboBox()
        self._power_combo.addItems([
            "Optimal Power",
            "Adaptive",
            "Prefer Maximum Performance"
        ])
        self._power_combo.setCurrentIndex(1)
        power_layout.addWidget(self._power_combo)
        power_layout.addStretch()
        perf_layout.addLayout(power_layout)

        layout.addWidget(perf_group)

        # Buttons
        btn_layout = QHBoxLayout()

        self._restore_btn = QPushButton("Restore Defaults")
        self._restore_btn.clicked.connect(self._restore_defaults)
        btn_layout.addWidget(self._restore_btn)

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

    def _restore_defaults(self) -> None:
        """Restore default settings."""
        self._preset_combo.setCurrentIndex(0)
        self._aa_combo.setCurrentIndex(1)
        self._tf_combo.setCurrentIndex(2)
        self._af_combo.setCurrentIndex(4)
        self._vsync_check.setChecked(True)
        self._triple_check.setChecked(False)
        self._fps_spin.setValue(0)
        self._power_combo.setCurrentIndex(1)

    def set_profile(self, profile: Optional[GPUProfile]) -> None:
        """Update panel based on selected profile."""
        self._current_profile = profile
        self.setEnabled(profile is not None)
