"""
GeForce Experience - Drivers Tab
Shows driver version, update status, and driver history.
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QScrollArea, QPushButton, QProgressBar
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer

# Add project path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from geforce_experience.gfe_style import (
    GFE_GREEN, GFE_DARK_GRAY, GFE_MEDIUM_GRAY, GFE_TEXT_SECONDARY,
    GFE_ACCENT_YELLOW
)


class DriversTab(QWidget):
    """Drivers tab showing driver information and updates."""

    def __init__(self, gpu_profile=None):
        super().__init__()
        self._profile = gpu_profile
        self._timer = None  # Timer for download simulation
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(20)

        # Current driver section
        current_section = self._create_current_driver_section()
        layout.addWidget(current_section)

        # Available update section
        update_section = self._create_update_section()
        layout.addWidget(update_section)

        # Driver history
        history_section = self._create_history_section()
        layout.addWidget(history_section, 1)

    def _create_current_driver_section(self) -> QWidget:
        """Create current driver info card."""
        frame = QFrame()
        frame.setProperty("card", True)
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {GFE_DARK_GRAY};
                border-radius: 12px;
                padding: 25px;
                border-left: 4px solid {GFE_GREEN};
            }}
        """)

        layout = QVBoxLayout(frame)

        header = QHBoxLayout()

        # Driver info
        left = QVBoxLayout()

        title = QLabel("Current Driver")
        title.setStyleSheet(f"color: {GFE_TEXT_SECONDARY}; font-size: 12px;")
        left.addWidget(title)

        driver_ver = self._profile.driver_version if self._profile else "551.86"
        version = QLabel(f"Game Ready Driver {driver_ver}")
        version.setFont(QFont("Segoe UI", 20, QFont.Bold))
        left.addWidget(version)

        gpu_name = self._profile.name if self._profile else "NVIDIA GeForce RTX 4090"
        gpu_label = QLabel(f"Installed on: {gpu_name}")
        gpu_label.setStyleSheet(f"color: {GFE_TEXT_SECONDARY};")
        left.addWidget(gpu_label)

        header.addLayout(left)
        header.addStretch()

        # Status badge
        status_frame = QFrame()
        status_frame.setStyleSheet(f"""
            QFrame {{
                background-color: rgba(118, 185, 0, 0.2);
                border-radius: 20px;
                padding: 10px 20px;
            }}
        """)
        status_layout = QHBoxLayout(status_frame)
        status_layout.setContentsMargins(15, 8, 15, 8)

        status = QLabel("Up to Date")
        status.setStyleSheet(f"color: {GFE_GREEN}; font-weight: bold;")
        status_layout.addWidget(status)

        header.addWidget(status_frame)

        layout.addLayout(header)

        # Additional info
        info_layout = QHBoxLayout()
        info_layout.setSpacing(40)

        install_date = (datetime.now() - timedelta(days=7)).strftime("%B %d, %Y")
        infos = [
            ("Release Date", "December 5, 2024"),
            ("Install Date", install_date),
            ("Driver Type", "DCH"),
            ("Windows Version", "Windows 11 64-bit"),
        ]

        for label, value in infos:
            info = QVBoxLayout()
            lbl = QLabel(label)
            lbl.setStyleSheet(f"color: {GFE_TEXT_SECONDARY}; font-size: 11px;")
            info.addWidget(lbl)
            val = QLabel(value)
            val.setFont(QFont("Segoe UI", 11, QFont.Bold))
            info.addWidget(val)
            info_layout.addLayout(info)

        info_layout.addStretch()
        layout.addLayout(info_layout)

        return frame

    def _create_update_section(self) -> QWidget:
        """Create the update available section."""
        frame = QFrame()
        frame.setProperty("card", True)
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {GFE_DARK_GRAY};
                border-radius: 12px;
                padding: 20px;
            }}
        """)

        layout = QHBoxLayout(frame)

        # Info
        left = QVBoxLayout()

        badge = QLabel("NEW")
        badge.setStyleSheet(f"""
            background-color: {GFE_ACCENT_YELLOW};
            color: {GFE_DARK_GRAY};
            font-weight: bold;
            font-size: 10px;
            padding: 3px 8px;
            border-radius: 3px;
        """)
        badge.setFixedWidth(50)
        left.addWidget(badge)

        title = QLabel("Game Ready Driver 552.12 Available")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        left.addWidget(title)

        desc = QLabel("Provides optimal support for the latest games and features")
        desc.setStyleSheet(f"color: {GFE_TEXT_SECONDARY};")
        left.addWidget(desc)

        layout.addLayout(left)
        layout.addStretch()

        # Buttons
        right = QVBoxLayout()
        right.setAlignment(Qt.AlignCenter)

        download_btn = QPushButton("Download")
        download_btn.setMinimumWidth(140)
        download_btn.clicked.connect(self._simulate_download)
        right.addWidget(download_btn)

        self._progress = QProgressBar()
        self._progress.setVisible(False)
        self._progress.setMinimumWidth(140)
        right.addWidget(self._progress)

        layout.addLayout(right)

        return frame

    def _simulate_download(self):
        """Simulate a driver download."""
        self._progress.setVisible(True)
        self._progress.setValue(0)

        # Create timer with parent to ensure proper cleanup
        if self._timer:
            self._timer.stop()
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_progress)
        self._timer.start(50)

    def _update_progress(self):
        """Update the progress bar."""
        current = self._progress.value()
        if current >= 100:
            self._timer.stop()
            self._progress.setFormat("Download Complete!")
        else:
            self._progress.setValue(current + 1)

    def _create_history_section(self) -> QWidget:
        """Create driver history section."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("Driver History")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        layout.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        history_widget = QWidget()
        history_layout = QVBoxLayout(history_widget)
        history_layout.setSpacing(10)

        # Mock driver history
        history = [
            ("551.86", "December 5, 2024", "Game Ready", True),
            ("551.61", "November 20, 2024", "Game Ready", False),
            ("551.52", "November 12, 2024", "Studio", False),
            ("551.23", "October 30, 2024", "Game Ready", False),
            ("550.90", "October 15, 2024", "Game Ready", False),
        ]

        for version, date, driver_type, is_current in history:
            card = self._create_history_card(version, date, driver_type, is_current)
            history_layout.addWidget(card)

        history_layout.addStretch()
        scroll.setWidget(history_widget)
        layout.addWidget(scroll)

        return container

    def _create_history_card(self, version: str, date: str, driver_type: str, is_current: bool) -> QFrame:
        """Create a driver history card."""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {GFE_DARK_GRAY};
                border-radius: 8px;
                padding: 12px 15px;
                {'border-left: 3px solid ' + GFE_GREEN + ';' if is_current else ''}
            }}
        """)

        layout = QHBoxLayout(card)

        # Version info
        version_label = QLabel(f"v{version}")
        version_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        version_label.setMinimumWidth(80)
        layout.addWidget(version_label)

        # Type badge
        type_color = GFE_GREEN if driver_type == "Game Ready" else GFE_ACCENT_YELLOW
        type_label = QLabel(driver_type)
        type_label.setStyleSheet(f"""
            background-color: rgba({int(type_color[1:3], 16)}, {int(type_color[3:5], 16)}, {int(type_color[5:7], 16)}, 0.2);
            color: {type_color};
            padding: 3px 10px;
            border-radius: 3px;
            font-size: 11px;
        """)
        layout.addWidget(type_label)

        layout.addStretch()

        # Date
        date_label = QLabel(date)
        date_label.setStyleSheet(f"color: {GFE_TEXT_SECONDARY};")
        layout.addWidget(date_label)

        if is_current:
            current_badge = QLabel("INSTALLED")
            current_badge.setStyleSheet(f"""
                background-color: {GFE_GREEN};
                color: {GFE_DARK_GRAY};
                font-weight: bold;
                font-size: 10px;
                padding: 3px 10px;
                border-radius: 3px;
            """)
            layout.addWidget(current_badge)

        return card

    def set_profile(self, profile):
        """Update the GPU profile."""
        self._profile = profile
