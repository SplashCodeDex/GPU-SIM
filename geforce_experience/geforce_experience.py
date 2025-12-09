"""
GeForce Experience - Main Application
A replica of NVIDIA GeForce Experience showing spoofed GPU information.
"""

import sys
import os
from pathlib import Path
from typing import Optional

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTabWidget, QFrame, QMenuBar, QMenu, QAction,
    QStatusBar, QSystemTrayIcon, QMessageBox
)
from PyQt5.QtGui import QFont, QIcon, QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt

# Add project path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from geforce_experience.gfe_style import get_gfe_stylesheet, GFE_GREEN, GFE_DARK_GRAY
from geforce_experience.tabs.home_tab import HomeTab
from geforce_experience.tabs.games_tab import GamesTab
from geforce_experience.tabs.drivers_tab import DriversTab
from geforce_experience.tabs.settings_tab import SettingsTab
from src.core.config_manager import get_config_manager
from src.core.gpu_profile import GPUProfile


class GeForceExperience(QMainWindow):
    """Main GeForce Experience application window."""

    def __init__(self, profile: Optional[GPUProfile] = None):
        super().__init__()
        self._current_profile = profile or self._load_active_profile()
        self._tray_icon = None

        self.setWindowTitle("GeForce Experience")
        self.setMinimumSize(1100, 700)
        self.resize(1200, 800)

        # Set window icon
        self._set_window_icon()

        # Apply stylesheet
        self.setStyleSheet(get_gfe_stylesheet())

        # Setup UI
        self._setup_ui()
        self._create_menus()
        self._setup_tray_icon()

        # Center window
        self._center_window()

    def _load_active_profile(self) -> Optional[GPUProfile]:
        """Load the currently active GPU profile."""
        try:
            config_manager = get_config_manager()
            return config_manager.get_active_profile()
        except Exception:
            return None

    def _set_window_icon(self):
        """Set the window icon."""
        icon_path = project_root / "Agenda" / "512x512.png"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

    def _center_window(self):
        """Center the window on screen."""
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def _setup_ui(self):
        """Setup the main user interface."""
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        header = self._create_header()
        main_layout.addWidget(header)

        # Tab widget
        self._tab_widget = QTabWidget()
        self._tab_widget.setDocumentMode(True)

        # Create tabs
        self._home_tab = HomeTab(self._current_profile)
        self._games_tab = GamesTab(self._current_profile)
        self._drivers_tab = DriversTab(self._current_profile)
        self._settings_tab = SettingsTab(self._current_profile)

        self._tab_widget.addTab(self._home_tab, "HOME")
        self._tab_widget.addTab(self._games_tab, "GAMES")
        self._tab_widget.addTab(self._drivers_tab, "DRIVERS")
        self._tab_widget.addTab(self._settings_tab, "SETTINGS")

        main_layout.addWidget(self._tab_widget)

        # Status bar
        self._status_bar = QStatusBar()
        self._status_bar.showMessage(f"GeForce Experience | {self._current_profile.name if self._current_profile else 'No GPU detected'}")
        self.setStatusBar(self._status_bar)

    def _create_header(self) -> QWidget:
        """Create the app header."""
        header = QFrame()
        header.setFixedHeight(70)
        header.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {GFE_DARK_GRAY}, stop:0.3 #1A1A1A, stop:0.7 #1A1A1A, stop:1 {GFE_DARK_GRAY});
                border-bottom: 1px solid #333;
            }}
        """)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(25, 10, 25, 10)

        # Logo
        logo_path = project_root / "Agenda" / "512x512.png"
        if logo_path.exists():
            logo_label = QLabel()
            pixmap = QPixmap(str(logo_path)).scaled(
                45, 45, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            logo_label.setPixmap(pixmap)
            layout.addWidget(logo_label)

        # Title
        title = QLabel("GeForce Experience")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setStyleSheet("color: white; margin-left: 15px;")
        layout.addWidget(title)

        layout.addStretch()

        # GPU info badge
        if self._current_profile:
            gpu_badge = QLabel(f"{self._current_profile.name}")
            gpu_badge.setStyleSheet(f"""
                background-color: rgba(118, 185, 0, 0.2);
                color: {GFE_GREEN};
                padding: 8px 15px;
                border-radius: 18px;
                font-weight: 500;
            """)
            layout.addWidget(gpu_badge)

        return header

    def _create_menus(self):
        """Create the menu bar."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self._force_close)
        file_menu.addAction(exit_action)

        # Help menu
        help_menu = menubar.addMenu("Help")

        about_action = QAction("About GeForce Experience", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

        feedback_action = QAction("Send Feedback", self)
        help_menu.addAction(feedback_action)

        help_menu.addSeparator()

        check_update = QAction("Check for Updates", self)
        help_menu.addAction(check_update)

    def _setup_tray_icon(self):
        """Setup the system tray icon."""
        if not QSystemTrayIcon.isSystemTrayAvailable():
            return

        # Create green N icon
        icon = self._create_tray_icon()

        self._tray_icon = QSystemTrayIcon(icon, self)
        self._tray_icon.setToolTip("GeForce Experience")

        # Context menu
        from PyQt5.QtWidgets import QMenu
        menu = QMenu()

        show_action = menu.addAction("Open GeForce Experience")
        show_action.triggered.connect(self._show_from_tray)

        menu.addSeparator()

        update_action = menu.addAction("Check for Updates")

        menu.addSeparator()

        exit_action = menu.addAction("Exit")
        exit_action.triggered.connect(self._force_close)

        self._tray_icon.setContextMenu(menu)
        self._tray_icon.activated.connect(self._on_tray_activated)
        self._tray_icon.show()

        # Show startup notification
        self._tray_icon.showMessage(
            "GeForce Experience",
            f"Running with {self._current_profile.name if self._current_profile else 'GPU'}",
            QSystemTrayIcon.Information,
            2000
        )

    def _create_tray_icon(self) -> QIcon:
        """Create a green NVIDIA-style tray icon."""
        size = 64
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        # Green background circle
        painter.setBrush(QColor(GFE_GREEN))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(4, 4, size - 8, size - 8)

        # White "G" letter
        painter.setPen(QColor("white"))
        font = QFont("Segoe UI", 28, QFont.Bold)
        painter.setFont(font)
        painter.drawText(pixmap.rect(), Qt.AlignCenter, "G")

        painter.end()
        return QIcon(pixmap)

    def _show_from_tray(self):
        """Show window from tray."""
        self.showNormal()
        self.activateWindow()
        self.raise_()

    def _on_tray_activated(self, reason):
        """Handle tray icon activation."""
        if reason == QSystemTrayIcon.DoubleClick:
            self._show_from_tray()

    def _show_about(self):
        """Show about dialog."""
        gpu_name = self._current_profile.name if self._current_profile else "N/A"
        driver = self._current_profile.driver_version if self._current_profile else "N/A"

        QMessageBox.about(
            self,
            "About GeForce Experience",
            f"""<h2>GeForce Experience</h2>
            <p>Version 3.28.0.417</p>
            <p><b>GPU:</b> {gpu_name}</p>
            <p><b>Driver:</b> {driver}</p>
            <hr>
            <p style="color: gray; font-size: 10px;">
            This is a simulation for testing purposes.<br>
            Part of the GPU-SIM project.
            </p>
            <p>© 2024 NVIDIA Corporation (Simulated)</p>
            """
        )

    def closeEvent(self, event):
        """Handle close event - minimize to tray."""
        if self._tray_icon and self._tray_icon.isVisible():
            event.ignore()
            self.hide()
            self._tray_icon.showMessage(
                "GeForce Experience",
                "Application minimized to tray",
                QSystemTrayIcon.Information,
                1500
            )
        else:
            event.accept()

    def _force_close(self):
        """Force close the application."""
        if self._tray_icon:
            self._tray_icon.hide()
        QApplication.quit()


def main():
    """Main entry point."""
    # High DPI support - MUST be set BEFORE QApplication is created
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setApplicationName("GeForce Experience")
    app.setOrganizationName("NVIDIA Corporation")

    window = GeForceExperience()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
