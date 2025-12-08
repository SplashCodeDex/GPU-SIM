"""
GPU Selector Widget
Dropdown widget for selecting GPU profiles.
"""

from typing import Optional, List, Callable
from PyQt5.QtWidgets import (
    QWidget, QComboBox, QLabel, QVBoxLayout, QHBoxLayout,
    QGroupBox, QPushButton
)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont

import sys
sys.path.insert(0, str(__file__).rsplit('src', 1)[0])

from src.core.gpu_profile import GPUProfile
from src.core.config_manager import ConfigManager


class GPUSelector(QWidget):
    """
    Widget for selecting GPU profiles from a dropdown.
    Emits signal when selection changes.
    """

    profile_changed = pyqtSignal(object)  # Emits GPUProfile or None

    def __init__(self, config_manager: ConfigManager, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self._config_manager = config_manager
        self._profiles: List[GPUProfile] = []
        self._current_profile: Optional[GPUProfile] = None

        self._setup_ui()
        self._load_profiles()

    def _setup_ui(self) -> None:
        """Set up the widget UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Group box for styling
        group = QGroupBox("Virtual GPU Profile")
        group_layout = QVBoxLayout(group)

        # Profile dropdown
        self._combo = QComboBox()
        self._combo.setMinimumWidth(250)
        self._combo.currentIndexChanged.connect(self._on_selection_changed)
        group_layout.addWidget(self._combo)

        # Info label
        self._info_label = QLabel("Select a GPU profile")
        self._info_label.setStyleSheet("color: gray; font-size: 11px;")
        group_layout.addWidget(self._info_label)

        # Buttons row
        btn_layout = QHBoxLayout()

        self._refresh_btn = QPushButton("↻ Refresh")
        self._refresh_btn.clicked.connect(self._load_profiles)
        btn_layout.addWidget(self._refresh_btn)

        btn_layout.addStretch()
        group_layout.addLayout(btn_layout)

        layout.addWidget(group)

    def _load_profiles(self) -> None:
        """Load profiles into the dropdown."""
        self._combo.blockSignals(True)
        self._combo.clear()

        # Reload profiles
        self._config_manager.load_profiles()
        self._profiles = self._config_manager.list_profiles()

        # Add "None" option
        self._combo.addItem("-- Select a GPU --", None)

        # Group by manufacturer
        nvidia_profiles = []
        amd_profiles = []
        other_profiles = []

        for profile in self._profiles:
            if profile.is_nvidia:
                nvidia_profiles.append(profile)
            elif profile.is_amd:
                amd_profiles.append(profile)
            else:
                other_profiles.append(profile)

        # Add NVIDIA profiles
        if nvidia_profiles:
            self._combo.insertSeparator(self._combo.count())
            for profile in nvidia_profiles:
                self._combo.addItem(f"🟢 {profile.name}", profile)

        # Add AMD profiles
        if amd_profiles:
            self._combo.insertSeparator(self._combo.count())
            for profile in amd_profiles:
                self._combo.addItem(f"🔴 {profile.name}", profile)

        # Add other profiles
        if other_profiles:
            self._combo.insertSeparator(self._combo.count())
            for profile in other_profiles:
                self._combo.addItem(profile.name, profile)

        self._combo.blockSignals(False)

        # Update info
        self._info_label.setText(f"{len(self._profiles)} profile(s) available")

    def _on_selection_changed(self, index: int) -> None:
        """Handle dropdown selection change."""
        profile = self._combo.currentData()
        self._current_profile = profile

        if profile:
            self._info_label.setText(
                f"{profile.vram_gb:.0f}GB {profile.vram_type} | Driver: {profile.driver_version}"
            )
        else:
            self._info_label.setText("Select a GPU profile")

        self.profile_changed.emit(profile)

    @property
    def current_profile(self) -> Optional[GPUProfile]:
        """Get the currently selected profile."""
        return self._current_profile

    def set_profile(self, profile_id: str) -> bool:
        """Set the selected profile by ID."""
        for i in range(self._combo.count()):
            profile = self._combo.itemData(i)
            if profile and profile.id == profile_id:
                self._combo.setCurrentIndex(i)
                return True
        return False
