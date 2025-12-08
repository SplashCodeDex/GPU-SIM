"""
Display Settings Panel
Shows display/resolution settings similar to NVIDIA Control Panel.
"""

from typing import Optional, List
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox,
    QFormLayout, QComboBox, QListWidget, QListWidgetItem, QPushButton,
    QScrollArea, QFrame
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.gpu_profile import GPUProfile


class DisplaySettingsPanel(QWidget):
    """
    Display settings panel for resolution and refresh rate.
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
        header = QLabel("Change resolution")
        header.setFont(QFont("Segoe UI", 16, QFont.Bold))
        layout.addWidget(header)

        # Display selector
        display_group = QGroupBox("1. Select the display you would like to change")
        display_layout = QVBoxLayout(display_group)

        self._display_combo = QComboBox()
        self._display_combo.addItems([
            "1. Display - Generic PnP Monitor (NVIDIA GeForce)",
        ])
        display_layout.addWidget(self._display_combo)

        layout.addWidget(display_group)

        # Resolution selector
        res_group = QGroupBox("2. Apply the following settings")
        res_layout = QVBoxLayout(res_group)

        # Resolution list
        res_label = QLabel("Resolution:")
        res_layout.addWidget(res_label)

        self._resolution_list = QListWidget()
        self._resolution_list.setMaximumHeight(200)
        res_layout.addWidget(self._resolution_list)

        # Refresh rate
        refresh_layout = QHBoxLayout()
        refresh_layout.addWidget(QLabel("Refresh rate:"))

        self._refresh_combo = QComboBox()
        self._refresh_combo.setMinimumWidth(150)
        refresh_layout.addWidget(self._refresh_combo)
        refresh_layout.addStretch()

        res_layout.addLayout(refresh_layout)

        # Color depth
        color_layout = QHBoxLayout()
        color_layout.addWidget(QLabel("Output color depth:"))

        self._color_combo = QComboBox()
        self._color_combo.addItems(["8 bpc", "10 bpc", "12 bpc"])
        self._color_combo.setCurrentText("8 bpc")
        color_layout.addWidget(self._color_combo)
        color_layout.addStretch()

        res_layout.addLayout(color_layout)

        layout.addWidget(res_group)

        # Apply button
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        apply_btn = QPushButton("Apply")
        apply_btn.setStyleSheet("background-color: #76B900; color: white;")
        btn_layout.addWidget(apply_btn)

        layout.addLayout(btn_layout)

        layout.addStretch()

        # Load default resolutions
        self._load_default_resolutions()

    def _load_default_resolutions(self) -> None:
        """Load default resolution options."""
        resolutions = [
            "3840 x 2160",
            "2560 x 1440",
            "1920 x 1080",
            "1680 x 1050",
            "1600 x 900",
            "1440 x 900",
            "1366 x 768",
            "1280 x 1024",
            "1280 x 720",
        ]

        for res in resolutions:
            item = QListWidgetItem(res)
            self._resolution_list.addItem(item)

        # Select 1920x1080 by default
        for i in range(self._resolution_list.count()):
            if "1920 x 1080" in self._resolution_list.item(i).text():
                self._resolution_list.setCurrentRow(i)
                break

        # Load refresh rates
        self._refresh_combo.addItems([
            "60 Hz",
            "75 Hz",
            "120 Hz",
            "144 Hz",
            "165 Hz",
            "240 Hz",
        ])

    def set_profile(self, profile: Optional[GPUProfile]) -> None:
        """Set the GPU profile and update display modes."""
        self._profile = profile

        if not profile:
            return

        # Update display name
        self._display_combo.clear()
        self._display_combo.addItem(f"1. Display - Generic PnP Monitor ({profile.name})")

        # Update resolutions from profile if available
        if profile.display_modes:
            self._resolution_list.clear()
            seen = set()
            for mode in profile.display_modes:
                res = f"{mode.width} x {mode.height}"
                if res not in seen:
                    self._resolution_list.addItem(res)
                    seen.add(res)

            # Update refresh rates
            self._refresh_combo.clear()
            refresh_rates = sorted(set(m.refresh for m in profile.display_modes), reverse=True)
            for rate in refresh_rates:
                self._refresh_combo.addItem(f"{rate} Hz")
