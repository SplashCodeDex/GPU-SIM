"""
GeForce Experience - Home Tab
Displays game library, driver status, and system info.
"""

import sys
from pathlib import Path
from typing import Optional

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QScrollArea, QGridLayout, QPushButton
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# Add project path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from geforce_experience.gfe_style import (
    GFE_GREEN, GFE_DARK_GRAY, GFE_MEDIUM_GRAY, GFE_TEXT_SECONDARY
)


class HomeTab(QWidget):
    """Home tab showing games and quick actions."""

    def __init__(self, gpu_profile=None):
        super().__init__()
        self._profile = gpu_profile
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(25)

        # Welcome section
        welcome_section = self._create_welcome_section()
        layout.addWidget(welcome_section)

        # Quick actions
        actions_section = self._create_quick_actions()
        layout.addWidget(actions_section)

        # Game library
        games_section = self._create_games_section()
        layout.addWidget(games_section, 1)

    def _create_welcome_section(self) -> QWidget:
        """Create the welcome header."""
        frame = QFrame()
        frame.setProperty("card", True)
        frame.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {GFE_DARK_GRAY}, stop:1 {GFE_MEDIUM_GRAY});
                border-radius: 12px;
                padding: 25px;
            }}
        """)

        layout = QHBoxLayout(frame)

        # Left side - welcome text
        left = QVBoxLayout()

        title = QLabel("Welcome to GeForce Experience")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        left.addWidget(title)

        gpu_name = self._profile.name if self._profile else "NVIDIA GeForce RTX 4090"
        subtitle = QLabel(f"Your GPU: {gpu_name}")
        subtitle.setStyleSheet(f"color: {GFE_GREEN}; font-size: 16px;")
        left.addWidget(subtitle)

        status = QLabel("✓ All drivers are up to date")
        status.setStyleSheet(f"color: {GFE_TEXT_SECONDARY}; font-size: 13px; margin-top: 10px;")
        left.addWidget(status)

        layout.addLayout(left)
        layout.addStretch()

        # Right side - quick stats
        right = QVBoxLayout()
        right.setAlignment(Qt.AlignRight | Qt.AlignTop)

        games_count = QLabel("12")
        games_count.setFont(QFont("Segoe UI", 36, QFont.Bold))
        games_count.setStyleSheet(f"color: {GFE_GREEN};")
        games_count.setAlignment(Qt.AlignCenter)
        right.addWidget(games_count)

        games_label = QLabel("Games Optimized")
        games_label.setStyleSheet(f"color: {GFE_TEXT_SECONDARY};")
        games_label.setAlignment(Qt.AlignCenter)
        right.addWidget(games_label)

        layout.addLayout(right)

        return frame

    def _create_quick_actions(self) -> QWidget:
        """Create quick action buttons."""
        frame = QFrame()
        layout = QHBoxLayout(frame)
        layout.setSpacing(15)

        actions = [
            ("🔄", "Check for Updates", "Scan for driver updates"),
            ("⚡", "Optimize Games", "Apply optimal settings"),
            ("📹", "ShadowPlay", "Record gameplay"),
            ("📸", "Screenshot", "Capture game moments"),
        ]

        for icon, title, desc in actions:
            btn = self._create_action_card(icon, title, desc)
            layout.addWidget(btn)

        return frame

    def _create_action_card(self, icon: str, title: str, desc: str) -> QFrame:
        """Create a quick action card."""
        card = QFrame()
        card.setProperty("card", True)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {GFE_DARK_GRAY};
                border-radius: 8px;
                padding: 15px;
            }}
            QFrame:hover {{
                background-color: {GFE_MEDIUM_GRAY};
                border: 1px solid {GFE_GREEN};
            }}
        """)
        card.setCursor(Qt.PointingHandCursor)
        card.setMinimumHeight(100)

        layout = QVBoxLayout(card)
        layout.setAlignment(Qt.AlignCenter)

        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Segoe UI Emoji", 28))
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)

        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        desc_label = QLabel(desc)
        desc_label.setStyleSheet(f"color: {GFE_TEXT_SECONDARY}; font-size: 11px;")
        desc_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc_label)

        return card

    def _create_games_section(self) -> QWidget:
        """Create the games library section."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)

        # Header
        header = QHBoxLayout()
        title = QLabel("Your Games")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        header.addWidget(title)

        header.addStretch()

        scan_btn = QPushButton("Scan for Games")
        scan_btn.setMaximumWidth(150)
        header.addWidget(scan_btn)

        layout.addLayout(header)

        # Games grid (mock data)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        grid_widget = QWidget()
        grid = QGridLayout(grid_widget)
        grid.setSpacing(15)

        # Mock games
        games = [
            ("Cyberpunk 2077", "Optimal", "CD PROJEKT RED"),
            ("Elden Ring", "Optimal", "FromSoftware"),
            ("Hogwarts Legacy", "Optimal", "Portkey Games"),
            ("Forza Horizon 5", "Optimal", "Playground Games"),
            ("Call of Duty: MW3", "Not Optimized", "Activision"),
            ("Baldur's Gate 3", "Optimal", "Larian Studios"),
            ("Starfield", "Optimal", "Bethesda"),
            ("Diablo IV", "Optimal", "Blizzard"),
        ]

        for i, (name, status, dev) in enumerate(games):
            card = self._create_game_card(name, status, dev)
            grid.addWidget(card, i // 4, i % 4)

        scroll.setWidget(grid_widget)
        layout.addWidget(scroll)

        return container

    def _create_game_card(self, name: str, status: str, dev: str) -> QFrame:
        """Create a game card."""
        card = QFrame()
        card.setProperty("card", True)
        card.setMinimumSize(200, 150)
        card.setMaximumWidth(250)
        card.setCursor(Qt.PointingHandCursor)

        border_color = GFE_GREEN if status == "Optimal" else "#FF6B6B"
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {GFE_DARK_GRAY};
                border-radius: 8px;
                border-bottom: 3px solid {border_color};
            }}
            QFrame:hover {{
                background-color: {GFE_MEDIUM_GRAY};
            }}
        """)

        layout = QVBoxLayout(card)
        layout.setAlignment(Qt.AlignTop)

        # Game icon placeholder
        icon = QLabel("🎮")
        icon.setFont(QFont("Segoe UI Emoji", 36))
        icon.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon)

        # Game name
        name_label = QLabel(name)
        name_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setWordWrap(True)
        layout.addWidget(name_label)

        # Developer
        dev_label = QLabel(dev)
        dev_label.setStyleSheet(f"color: {GFE_TEXT_SECONDARY}; font-size: 10px;")
        dev_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(dev_label)

        # Status
        status_color = GFE_GREEN if status == "Optimal" else "#FF6B6B"
        status_label = QLabel(f"● {status}")
        status_label.setStyleSheet(f"color: {status_color}; font-size: 11px;")
        status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(status_label)

        return card

    def set_profile(self, profile):
        """Update the GPU profile."""
        self._profile = profile
