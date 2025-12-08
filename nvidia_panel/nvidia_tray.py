"""
NVIDIA System Tray Icon
Provides a realistic NVIDIA system tray icon with the green "N" logo.
"""

import sys
from pathlib import Path
from typing import Optional

from PyQt5.QtWidgets import (
    QSystemTrayIcon, QMenu, QAction, QApplication, QMessageBox
)
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QFont, QBrush
from PyQt5.QtCore import Qt, pyqtSignal, QObject

# NVIDIA brand color
NVIDIA_GREEN = "#76B900"

project_root = Path(__file__).parent.parent


def create_nvidia_icon() -> QIcon:
    """
    Create an NVIDIA-style green "N" icon for the system tray.
    Similar to the real NVIDIA tray icon.
    """
    # Try to load custom icon first
    icon_paths = [
        project_root / "Agenda" / "512x512.png",
        project_root / "assets" / "icons" / "nvidia.ico",
    ]

    for path in icon_paths:
        if path.exists():
            return QIcon(str(path))

    # Create a programmatic NVIDIA-style icon
    size = 64
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)

    # Green background circle
    painter.setBrush(QBrush(QColor(NVIDIA_GREEN)))
    painter.setPen(Qt.NoPen)
    painter.drawEllipse(2, 2, size - 4, size - 4)

    # White "N" letter
    painter.setPen(QColor("white"))
    font = QFont("Arial Black", 32, QFont.Bold)
    painter.setFont(font)
    painter.drawText(pixmap.rect(), Qt.AlignCenter, "N")

    painter.end()

    return QIcon(pixmap)


class NVIDIATrayIcon(QSystemTrayIcon):
    """
    NVIDIA System Tray Icon.
    Provides quick access to NVIDIA Control Panel and settings.
    """

    # Signals
    show_control_panel = pyqtSignal()
    open_settings = pyqtSignal()

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)

        self.setIcon(create_nvidia_icon())
        self.setToolTip("NVIDIA Settings")

        self._setup_menu()

        # Show notification on startup (like real NVIDIA)
        self.activated.connect(self._on_activated)

    def _setup_menu(self) -> None:
        """Set up the context menu."""
        menu = QMenu()
        menu.setStyleSheet("""
            QMenu {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #404040;
            }
            QMenu::item:selected {
                background-color: #76B900;
            }
        """)

        # NVIDIA Control Panel
        control_panel_action = QAction("NVIDIA Control Panel", self)
        control_panel_action.triggered.connect(self._on_control_panel)
        menu.addAction(control_panel_action)

        menu.addSeparator()

        # NVIDIA GeForce Experience (stub)
        geforce_action = QAction("NVIDIA GeForce Experience", self)
        geforce_action.triggered.connect(self._on_geforce_experience)
        menu.addAction(geforce_action)

        menu.addSeparator()

        # Open NVIDIA Settings
        settings_action = QAction("Open NVIDIA Settings", self)
        settings_action.triggered.connect(self._on_settings)
        menu.addAction(settings_action)

        # Check for updates
        updates_action = QAction("Check for updates", self)
        updates_action.triggered.connect(self._on_check_updates)
        menu.addAction(updates_action)

        menu.addSeparator()

        # Exit
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self._on_exit)
        menu.addAction(exit_action)

        self.setContextMenu(menu)

    def _on_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        """Handle tray icon activation."""
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_control_panel.emit()

    def _on_control_panel(self) -> None:
        """Open NVIDIA Control Panel."""
        self.show_control_panel.emit()

    def _on_geforce_experience(self) -> None:
        """Open GeForce Experience (stub)."""
        QMessageBox.information(
            None,
            "NVIDIA GeForce Experience",
            "GeForce Experience is not installed.\n\n"
            "Visit geforce.com to download."
        )

    def _on_settings(self) -> None:
        """Open NVIDIA settings."""
        self.open_settings.emit()

    def _on_check_updates(self) -> None:
        """Check for driver updates."""
        QMessageBox.information(
            None,
            "NVIDIA Update",
            "Your NVIDIA driver is up to date.\n\n"
            "Current version: Game Ready Driver"
        )

    def _on_exit(self) -> None:
        """Exit the application."""
        QApplication.quit()

    def show_startup_notification(self) -> None:
        """Show startup notification like real NVIDIA driver."""
        if self.supportsMessages():
            self.showMessage(
                "NVIDIA Settings",
                "NVIDIA driver loaded successfully.",
                QSystemTrayIcon.Information,
                2000
            )
