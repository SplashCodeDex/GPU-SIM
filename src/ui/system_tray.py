"""
System Tray Integration
Provides system tray icon with quick profile switching and status display.
"""

import sys
import logging
from typing import Optional, List
from pathlib import Path

from PyQt5.QtWidgets import (
    QSystemTrayIcon, QMenu, QAction, QApplication, QStyle
)
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
from PyQt5.QtCore import QObject, pyqtSignal

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.config_manager import get_config_manager
from src.core.gpu_profile import GPUProfile

logger = logging.getLogger(__name__)


class SystemTrayManager(QObject):
    """
    Manages the system tray icon and menu.
    """

    # Signals
    profile_selected = pyqtSignal(object)  # GPUProfile or None
    show_window_requested = pyqtSignal()
    quit_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self._config_manager = get_config_manager()
        self._current_profile: Optional[GPUProfile] = None

        # Create tray icon
        self._tray_icon = QSystemTrayIcon(parent)
        self._update_icon()

        # Create menu
        self._create_menu()

        # Connect signals
        self._tray_icon.activated.connect(self._on_activated)

        logger.info("SystemTrayManager initialized")

    def _create_gpu_icon(self, color: QColor = QColor(118, 185, 0)) -> QIcon:
        """Create a simple GPU icon."""
        pixmap = QPixmap(64, 64)
        pixmap.fill(QColor(0, 0, 0, 0))

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw GPU shape
        painter.setBrush(color)
        painter.setPen(color.darker(120))
        painter.drawRoundedRect(8, 16, 48, 32, 4, 4)

        # Fan circles
        painter.setBrush(color.darker(150))
        painter.drawEllipse(16, 24, 16, 16)
        painter.drawEllipse(36, 24, 16, 16)

        painter.end()
        return QIcon(pixmap)

    def _update_icon(self) -> None:
        """Update the tray icon based on current state."""
        # Try to load custom icon first
        icon_paths = [
            project_root / "assets" / "icons" / "gpu_sim.ico",
            project_root / "assets" / "icons" / "nvidia.ico",
        ]

        icon = None
        for path in icon_paths:
            if path.exists():
                icon = QIcon(str(path))
                break

        if not icon:
            # Create a simple GPU-themed icon
            if self._current_profile:
                # Green for active profile
                icon = self._create_gpu_icon(QColor(118, 185, 0))
            else:
                # Gray for no profile
                icon = self._create_gpu_icon(QColor(100, 100, 100))

        self._tray_icon.setIcon(icon)
        self._update_tooltip()

    def _update_tooltip(self) -> None:
        """Update the tray icon tooltip."""
        if self._current_profile:
            tooltip = f"GPU-SIM: {self._current_profile.name}"
        else:
            tooltip = "GPU-SIM: No profile active"

        self._tray_icon.setToolTip(tooltip)

    def _create_menu(self) -> None:
        """Create the tray context menu."""
        menu = QMenu()
        menu.setStyleSheet("""
            QMenu {
                background-color: #2d2d2d;
                color: #cccccc;
                border: 1px solid #3d3d3d;
            }
            QMenu::item:selected {
                background-color: #094771;
            }
            QMenu::separator {
                background-color: #3d3d3d;
                height: 1px;
            }
        """)

        # Status
        self._status_action = QAction("GPU-SIM", menu)
        self._status_action.setEnabled(False)
        menu.addAction(self._status_action)
        menu.addSeparator()

        # Quick profile selection
        self._profiles_menu = menu.addMenu("🎮 Select Profile")
        self._update_profiles_menu()

        menu.addSeparator()

        # Show main window
        show_action = QAction("🖥️ Open Control Panel", menu)
        show_action.triggered.connect(self._on_show_window)
        menu.addAction(show_action)

        # Separator
        menu.addSeparator()

        # Start with Windows
        self._startup_action = QAction("🚀 Start with Windows", menu)
        self._startup_action.setCheckable(True)
        self._startup_action.setChecked(self._is_startup_enabled())
        self._startup_action.triggered.connect(self._toggle_startup)
        menu.addAction(self._startup_action)

        menu.addSeparator()

        # Quit
        quit_action = QAction("❌ Quit", menu)
        quit_action.triggered.connect(self._on_quit)
        menu.addAction(quit_action)

        self._tray_icon.setContextMenu(menu)

    def _update_profiles_menu(self) -> None:
        """Update the profiles submenu."""
        self._profiles_menu.clear()

        # Group by manufacturer
        profiles = self._config_manager.list_profiles()
        manufacturers = {}

        for profile in profiles:
            manufacturer = profile.manufacturer.split()[0]  # First word
            if manufacturer not in manufacturers:
                manufacturers[manufacturer] = []
            manufacturers[manufacturer].append(profile)

        # Add grouped profiles
        for manufacturer, profile_list in sorted(manufacturers.items()):
            submenu = self._profiles_menu.addMenu(manufacturer)

            for profile in sorted(profile_list, key=lambda p: p.name):
                action = QAction(profile.name, submenu)
                action.setCheckable(True)
                action.setChecked(self._current_profile == profile)
                action.triggered.connect(
                    lambda checked, p=profile: self._on_profile_selected(p)
                )
                submenu.addAction(action)

        # None option
        self._profiles_menu.addSeparator()
        none_action = QAction("(None)", self._profiles_menu)
        none_action.setCheckable(True)
        none_action.setChecked(self._current_profile is None)
        none_action.triggered.connect(lambda: self._on_profile_selected(None))
        self._profiles_menu.addAction(none_action)

    def _is_startup_enabled(self) -> bool:
        """Check if startup is enabled."""
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0, winreg.KEY_READ
            )
            try:
                winreg.QueryValueEx(key, "GPU-SIM")
                return True
            except FileNotFoundError:
                return False
            finally:
                winreg.CloseKey(key)
        except Exception:
            return False

    def _toggle_startup(self, enabled: bool) -> None:
        """Toggle startup with Windows."""
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0, winreg.KEY_SET_VALUE
            )

            if enabled:
                # Add to startup
                exe_path = sys.executable
                script_path = project_root / "src" / "main.py"
                command = f'"{exe_path}" "{script_path}" --tray'
                winreg.SetValueEx(key, "GPU-SIM", 0, winreg.REG_SZ, command)
                logger.info("Added to startup")
            else:
                # Remove from startup
                try:
                    winreg.DeleteValue(key, "GPU-SIM")
                    logger.info("Removed from startup")
                except FileNotFoundError:
                    pass

            winreg.CloseKey(key)
        except Exception as e:
            logger.error(f"Failed to toggle startup: {e}")

    def _on_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        """Handle tray icon activation."""
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_window_requested.emit()
        elif reason == QSystemTrayIcon.Trigger:
            # Left click - show menu
            self._tray_icon.contextMenu().popup(
                self._tray_icon.geometry().center()
            )

    def _on_profile_selected(self, profile: Optional[GPUProfile]) -> None:
        """Handle profile selection from tray menu."""
        self.set_profile(profile)
        self.profile_selected.emit(profile)

    def _on_show_window(self) -> None:
        """Handle show window request."""
        self.show_window_requested.emit()

    def _on_quit(self) -> None:
        """Handle quit request."""
        self.quit_requested.emit()

    def set_profile(self, profile: Optional[GPUProfile]) -> None:
        """Set the current profile."""
        self._current_profile = profile
        self._update_icon()
        self._update_profiles_menu()

        # Update status
        if profile:
            self._status_action.setText(f"🎮 {profile.name}")
            self._tray_icon.showMessage(
                "GPU-SIM",
                f"Profile changed to: {profile.name}",
                QSystemTrayIcon.Information,
                2000
            )
        else:
            self._status_action.setText("GPU-SIM")

    def show(self) -> None:
        """Show the tray icon."""
        self._tray_icon.show()

    def hide(self) -> None:
        """Hide the tray icon."""
        self._tray_icon.hide()

    @property
    def is_visible(self) -> bool:
        """Check if tray icon is visible."""
        return self._tray_icon.isVisible()


# Singleton
_tray_manager: Optional[SystemTrayManager] = None

def get_tray_manager() -> SystemTrayManager:
    """Get the singleton tray manager."""
    global _tray_manager
    if _tray_manager is None:
        _tray_manager = SystemTrayManager()
    return _tray_manager
