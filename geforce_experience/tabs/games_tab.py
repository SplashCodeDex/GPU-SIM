"""
GeForce Experience - Games Tab
Displays game library with optimization status and recommended settings.
"""

import sys
from pathlib import Path
from typing import Optional, List, Dict

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QGridLayout, QPushButton, QScrollArea, QLineEdit,
    QComboBox, QProgressBar
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# Add project path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from geforce_experience.gfe_style import (
    GFE_GREEN, GFE_DARK_GRAY, GFE_MEDIUM_GRAY, GFE_TEXT_SECONDARY
)


# Fake game database with optimization settings
GAME_DATABASE = [
    {
        "name": "Cyberpunk 2077",
        "developer": "CD Projekt Red",
        "status": "Optimized",
        "quality": "Ultra",
        "resolution": "1920x1080",
        "fps": "60",
        "ray_tracing": True,
        "dlss": "Quality",
        "icon": "🎮"
    },
    {
        "name": "Red Dead Redemption 2",
        "developer": "Rockstar Games",
        "status": "Optimized",
        "quality": "High",
        "resolution": "1920x1080",
        "fps": "60",
        "ray_tracing": False,
        "dlss": "Off",
        "icon": "🤠"
    },
    {
        "name": "Elden Ring",
        "developer": "FromSoftware",
        "status": "Optimized",
        "quality": "Maximum",
        "resolution": "1920x1080",
        "fps": "60",
        "ray_tracing": False,
        "dlss": "Off",
        "icon": "⚔️"
    },
    {
        "name": "Call of Duty: Warzone",
        "developer": "Infinity Ward",
        "status": "Needs Optimization",
        "quality": "Medium",
        "resolution": "1920x1080",
        "fps": "120",
        "ray_tracing": False,
        "dlss": "Performance",
        "icon": "🎯"
    },
    {
        "name": "Fortnite",
        "developer": "Epic Games",
        "status": "Optimized",
        "quality": "Epic",
        "resolution": "1920x1080",
        "fps": "144",
        "ray_tracing": True,
        "dlss": "Performance",
        "icon": "🏗️"
    },
    {
        "name": "GTA V",
        "developer": "Rockstar Games",
        "status": "Optimized",
        "quality": "Very High",
        "resolution": "1920x1080",
        "fps": "60",
        "ray_tracing": False,
        "dlss": "Off",
        "icon": "🚗"
    },
    {
        "name": "Minecraft RTX",
        "developer": "Mojang",
        "status": "Optimized",
        "quality": "Extreme",
        "resolution": "1920x1080",
        "fps": "60",
        "ray_tracing": True,
        "dlss": "Quality",
        "icon": "🧱"
    },
    {
        "name": "Apex Legends",
        "developer": "Respawn",
        "status": "Optimized",
        "quality": "High",
        "resolution": "1920x1080",
        "fps": "144",
        "ray_tracing": False,
        "dlss": "Off",
        "icon": "🔫"
    },
]


class GamesTab(QWidget):
    """Games tab showing game library with optimization controls."""

    def __init__(self, gpu_profile=None):
        super().__init__()
        self._profile = gpu_profile
        self._game_cards = []
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header with search
        header_layout = QHBoxLayout()

        title = QLabel("My Games")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setStyleSheet("color: white;")
        header_layout.addWidget(title)

        # Games count
        count_label = QLabel(f"{len(GAME_DATABASE)} games found")
        count_label.setStyleSheet(f"color: {GFE_TEXT_SECONDARY}; font-size: 14px;")
        header_layout.addWidget(count_label)

        header_layout.addStretch()

        # Search box
        self._search_box = QLineEdit()
        self._search_box.setPlaceholderText("Search games...")
        self._search_box.setFixedWidth(200)
        self._search_box.setStyleSheet(f"""
            QLineEdit {{
                background-color: {GFE_MEDIUM_GRAY};
                border: 1px solid #555;
                border-radius: 5px;
                padding: 8px 12px;
                color: white;
            }}
            QLineEdit:focus {{
                border-color: {GFE_GREEN};
            }}
        """)
        self._search_box.textChanged.connect(self._filter_games)
        header_layout.addWidget(self._search_box)

        # Filter dropdown
        self._filter_combo = QComboBox()
        self._filter_combo.addItems(["All Games", "Optimized", "Needs Optimization"])
        self._filter_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {GFE_MEDIUM_GRAY};
                border: 1px solid #555;
                border-radius: 5px;
                padding: 8px 12px;
                color: white;
                min-width: 150px;
            }}
        """)
        self._filter_combo.currentTextChanged.connect(self._filter_games)
        header_layout.addWidget(self._filter_combo)

        # Optimize All button
        optimize_all_btn = QPushButton("Optimize All Games")
        optimize_all_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {GFE_GREEN};
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #8bc34a;
            }}
        """)
        optimize_all_btn.clicked.connect(self._optimize_all)
        header_layout.addWidget(optimize_all_btn)

        layout.addLayout(header_layout)

        # Scrollable games grid
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)

        scroll_widget = QWidget()
        self._games_grid = QGridLayout(scroll_widget)
        self._games_grid.setSpacing(15)

        # Create game cards
        self._create_game_cards()

        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)

    def _create_game_cards(self) -> None:
        """Create game cards for the grid."""
        self._game_cards.clear()

        for i, game in enumerate(GAME_DATABASE):
            card = self._create_game_card(game)
            self._game_cards.append((game, card))
            row = i // 2
            col = i % 2
            self._games_grid.addWidget(card, row, col)

    def _create_game_card(self, game: Dict) -> QFrame:
        """Create a single game card."""
        card = QFrame()
        card.setFrameStyle(QFrame.Box | QFrame.Raised)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {GFE_MEDIUM_GRAY};
                border-radius: 8px;
                border: 1px solid #444;
            }}
            QFrame:hover {{
                border-color: {GFE_GREEN};
            }}
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)

        # Game header
        header = QHBoxLayout()

        icon_label = QLabel(game["icon"])
        icon_label.setFont(QFont("Segoe UI", 24))
        header.addWidget(icon_label)

        info_layout = QVBoxLayout()

        name_label = QLabel(game["name"])
        name_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        name_label.setStyleSheet("color: white;")
        info_layout.addWidget(name_label)

        dev_label = QLabel(game["developer"])
        dev_label.setStyleSheet(f"color: {GFE_TEXT_SECONDARY}; font-size: 11px;")
        info_layout.addWidget(dev_label)

        header.addLayout(info_layout, 1)

        # Status badge
        status = game["status"]
        status_color = GFE_GREEN if status == "Optimized" else "#f39c12"
        status_label = QLabel(f"● {status}")
        status_label.setStyleSheet(f"color: {status_color}; font-size: 11px; font-weight: bold;")
        status_label.setAlignment(Qt.AlignRight)
        header.addWidget(status_label)

        layout.addLayout(header)

        # Separator
        separator = QFrame()
        separator.setFrameStyle(QFrame.HLine)
        separator.setStyleSheet(f"background-color: #444;")
        separator.setFixedHeight(1)
        layout.addWidget(separator)

        # Settings grid
        settings_grid = QGridLayout()
        settings_grid.setSpacing(8)

        settings = [
            ("Quality:", game["quality"]),
            ("Resolution:", game["resolution"]),
            ("Target FPS:", game["fps"]),
            ("DLSS:", game["dlss"]),
        ]

        for i, (label, value) in enumerate(settings):
            lbl = QLabel(label)
            lbl.setStyleSheet(f"color: {GFE_TEXT_SECONDARY}; font-size: 10px;")
            val = QLabel(value)
            val.setStyleSheet("color: white; font-size: 10px; font-weight: bold;")
            settings_grid.addWidget(lbl, i // 2, (i % 2) * 2)
            settings_grid.addWidget(val, i // 2, (i % 2) * 2 + 1)

        layout.addLayout(settings_grid)

        # Ray Tracing indicator
        if game.get("ray_tracing"):
            rt_label = QLabel("✨ Ray Tracing Enabled")
            rt_label.setStyleSheet(f"color: {GFE_GREEN}; font-size: 10px; font-weight: bold;")
            layout.addWidget(rt_label)

        # Action buttons
        btn_layout = QHBoxLayout()

        optimize_btn = QPushButton("Optimize")
        optimize_btn.setEnabled(game["status"] != "Optimized")
        optimize_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {GFE_GREEN if game["status"] != "Optimized" else "#555"};
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 3px;
                font-size: 11px;
            }}
            QPushButton:hover:enabled {{
                background-color: #8bc34a;
            }}
            QPushButton:disabled {{
                background-color: #555;
                color: #888;
            }}
        """)
        btn_layout.addWidget(optimize_btn)

        details_btn = QPushButton("Details")
        details_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {GFE_GREEN};
                border: 1px solid {GFE_GREEN};
                padding: 6px 12px;
                border-radius: 3px;
                font-size: 11px;
            }}
            QPushButton:hover {{
                background-color: rgba(118, 185, 0, 0.2);
            }}
        """)
        btn_layout.addWidget(details_btn)

        layout.addLayout(btn_layout)

        return card

    def _filter_games(self) -> None:
        """Filter games based on search and status filter."""
        search_text = self._search_box.text().lower()
        filter_status = self._filter_combo.currentText()

        for game, card in self._game_cards:
            visible = True

            # Search filter
            if search_text and search_text not in game["name"].lower():
                visible = False

            # Status filter
            if filter_status == "Optimized" and game["status"] != "Optimized":
                visible = False
            elif filter_status == "Needs Optimization" and game["status"] == "Optimized":
                visible = False

            card.setVisible(visible)

    def _optimize_all(self) -> None:
        """Simulate optimizing all games."""
        for game, card in self._game_cards:
            if game["status"] != "Optimized":
                game["status"] = "Optimized"

        # Refresh cards
        for i in reversed(range(self._games_grid.count())):
            self._games_grid.itemAt(i).widget().setParent(None)

        self._create_game_cards()

    def set_profile(self, profile) -> None:
        """Update the GPU profile."""
        self._profile = profile
