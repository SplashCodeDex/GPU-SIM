"""
GeForce Experience - Settings Tab
Application settings and preferences.
"""

import sys
from pathlib import Path
from typing import Optional

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QScrollArea, QPushButton, QCheckBox, QComboBox, QSlider,
    QLineEdit, QGroupBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# Add project path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from geforce_experience.gfe_style import (
    GFE_GREEN, GFE_DARK_GRAY, GFE_MEDIUM_GRAY, GFE_TEXT_SECONDARY
)


class SettingsTab(QWidget):
    """Settings tab for GeForce Experience preferences."""

    def __init__(self, gpu_profile=None):
        super().__init__()
        self._profile = gpu_profile
        self._setup_ui()

    def _setup_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(20)

        # General section
        general = self._create_general_section()
        layout.addWidget(general)

        # Game optimization section
        optimization = self._create_optimization_section()
        layout.addWidget(optimization)

        # Overlay section
        overlay = self._create_overlay_section()
        layout.addWidget(overlay)

        # Account section
        account = self._create_account_section()
        layout.addWidget(account)

        layout.addStretch()

        scroll.setWidget(content)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)

    def _create_section(self, title: str) -> QFrame:
        """Create a settings section frame."""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {GFE_DARK_GRAY};
                border-radius: 12px;
                padding: 20px;
            }}
        """)

        layout = QVBoxLayout(frame)

        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        layout.addWidget(title_label)

        return frame

    def _create_general_section(self) -> QWidget:
        """Create general settings section."""
        frame = self._create_section("General")
        layout = frame.layout()

        # Language
        lang_row = QHBoxLayout()
        lang_label = QLabel("Language")
        lang_row.addWidget(lang_label)
        lang_row.addStretch()
        lang_combo = QComboBox()
        lang_combo.addItems(["English", "Español", "Français", "Deutsch", "日本語", "中文"])
        lang_combo.setMinimumWidth(200)
        lang_row.addWidget(lang_combo)
        layout.addLayout(lang_row)

        # Start with Windows
        start_check = QCheckBox("Start GeForce Experience with Windows")
        start_check.setChecked(True)
        layout.addWidget(start_check)

        # Minimize to tray
        tray_check = QCheckBox("Minimize to system tray on close")
        tray_check.setChecked(True)
        layout.addWidget(tray_check)

        # Desktop notifications
        notif_check = QCheckBox("Enable desktop notifications")
        notif_check.setChecked(True)
        layout.addWidget(notif_check)

        # Auto-update
        update_check = QCheckBox("Automatically download driver updates")
        update_check.setChecked(False)
        layout.addWidget(update_check)

        return frame

    def _create_optimization_section(self) -> QWidget:
        """Create game optimization settings section."""
        frame = self._create_section("Game Optimization")
        layout = frame.layout()

        # Auto-optimize
        auto_opt = QCheckBox("Automatically optimize newly added games")
        auto_opt.setChecked(True)
        layout.addWidget(auto_opt)

        # Optimization preset
        preset_row = QHBoxLayout()
        preset_label = QLabel("Optimization Preset")
        preset_row.addWidget(preset_label)
        preset_row.addStretch()
        preset_combo = QComboBox()
        preset_combo.addItems(["Quality", "Balanced", "Performance"])
        preset_combo.setCurrentIndex(1)
        preset_combo.setMinimumWidth(200)
        preset_row.addWidget(preset_combo)
        layout.addLayout(preset_row)

        # Resolution scale
        scale_row = QHBoxLayout()
        scale_label = QLabel("Target Resolution Scale")
        scale_row.addWidget(scale_label)
        scale_row.addStretch()
        scale_value = QLabel("100%")
        scale_value.setMinimumWidth(50)
        scale_row.addWidget(scale_value)
        layout.addLayout(scale_row)

        scale_slider = QSlider(Qt.Horizontal)
        scale_slider.setRange(50, 100)
        scale_slider.setValue(100)
        scale_slider.valueChanged.connect(lambda v: scale_value.setText(f"{v}%"))
        layout.addWidget(scale_slider)

        # Game scan locations
        scan_row = QHBoxLayout()
        scan_label = QLabel("Game Scan Locations")
        scan_row.addWidget(scan_label)
        scan_row.addStretch()
        add_btn = QPushButton("Add Location")
        add_btn.setMaximumWidth(120)
        scan_row.addWidget(add_btn)
        layout.addLayout(scan_row)

        # Default locations
        locations = [
            "C:\\Program Files (x86)\\Steam\\steamapps\\common",
            "C:\\Program Files\\Epic Games",
            "C:\\Games",
        ]

        for loc in locations:
            loc_label = QLabel(f"  📁 {loc}")
            loc_label.setStyleSheet(f"color: {GFE_TEXT_SECONDARY}; font-size: 11px;")
            layout.addWidget(loc_label)

        return frame

    def _create_overlay_section(self) -> QWidget:
        """Create in-game overlay settings section."""
        frame = self._create_section("In-Game Overlay")
        layout = frame.layout()

        # Enable overlay
        overlay_check = QCheckBox("Enable in-game overlay")
        overlay_check.setChecked(True)
        layout.addWidget(overlay_check)

        # Hotkey
        hotkey_row = QHBoxLayout()
        hotkey_label = QLabel("Overlay Hotkey")
        hotkey_row.addWidget(hotkey_label)
        hotkey_row.addStretch()
        hotkey_input = QLineEdit("Alt + Z")
        hotkey_input.setMaximumWidth(150)
        hotkey_input.setAlignment(Qt.AlignCenter)
        hotkey_row.addWidget(hotkey_input)
        layout.addLayout(hotkey_row)

        # Screenshot hotkey
        screenshot_row = QHBoxLayout()
        screenshot_label = QLabel("Screenshot Hotkey")
        screenshot_row.addWidget(screenshot_label)
        screenshot_row.addStretch()
        screenshot_input = QLineEdit("Alt + F1")
        screenshot_input.setMaximumWidth(150)
        screenshot_input.setAlignment(Qt.AlignCenter)
        screenshot_row.addWidget(screenshot_input)
        layout.addLayout(screenshot_row)

        # Instant Replay
        replay_check = QCheckBox("Enable Instant Replay")
        replay_check.setChecked(True)
        layout.addWidget(replay_check)

        # Replay length
        replay_row = QHBoxLayout()
        replay_label = QLabel("Instant Replay Length")
        replay_row.addWidget(replay_label)
        replay_row.addStretch()
        replay_combo = QComboBox()
        replay_combo.addItems(["30 seconds", "1 minute", "2 minutes", "5 minutes", "10 minutes", "20 minutes"])
        replay_combo.setCurrentIndex(2)
        replay_combo.setMinimumWidth(150)
        replay_row.addWidget(replay_combo)
        layout.addLayout(replay_row)

        # FPS counter
        fps_check = QCheckBox("Show FPS counter")
        fps_check.setChecked(True)
        layout.addWidget(fps_check)

        return frame

    def _create_account_section(self) -> QWidget:
        """Create account settings section."""
        frame = self._create_section("Account")
        layout = frame.layout()

        # Account info
        account_row = QHBoxLayout()

        avatar = QLabel("👤")
        avatar.setFont(QFont("Segoe UI Emoji", 36))
        avatar.setStyleSheet(f"""
            background-color: {GFE_MEDIUM_GRAY};
            border-radius: 30px;
            padding: 10px;
        """)
        account_row.addWidget(avatar)

        info = QVBoxLayout()
        email = QLabel("user@example.com")
        email.setFont(QFont("Segoe UI", 14, QFont.Bold))
        info.addWidget(email)

        member = QLabel("NVIDIA Member since 2020")
        member.setStyleSheet(f"color: {GFE_TEXT_SECONDARY};")
        info.addWidget(member)

        account_row.addLayout(info)
        account_row.addStretch()

        logout_btn = QPushButton("Sign Out")
        logout_btn.setProperty("secondary", True)
        logout_btn.setMaximumWidth(100)
        account_row.addWidget(logout_btn)

        layout.addLayout(account_row)

        # Privacy
        privacy_check = QCheckBox("Share anonymous usage data to improve GeForce Experience")
        privacy_check.setChecked(False)
        layout.addWidget(privacy_check)

        return frame

    def set_profile(self, profile):
        """Update the GPU profile."""
        self._profile = profile
