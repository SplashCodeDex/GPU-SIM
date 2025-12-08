"""
NVIDIA Control Panel - Main Window
A replica of the NVIDIA Control Panel that displays spoofed GPU information.
"""

import sys
import os
from pathlib import Path
from typing import Optional

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTreeWidget, QTreeWidgetItem, QStackedWidget, QSplitter,
    QFrame, QMenuBar, QMenu, QAction, QStatusBar, QMessageBox
)
from PyQt5.QtGui import QFont, QIcon, QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt

# Add project path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from nvidia_panel.nvidia_style import get_theme, NVIDIA_GREEN, NVIDIA_BLACK
from nvidia_panel.panels.system_info import SystemInfoPanel
from nvidia_panel.panels.manage_3d import Manage3DPanel
from nvidia_panel.panels.display_settings import DisplaySettingsPanel
from src.core.config_manager import get_config_manager
from src.core.gpu_profile import GPUProfile


class NVIDIAControlPanel(QMainWindow):
    """
    Fake NVIDIA Control Panel replica.
    Displays GPU information matching the spoofed profile.
    """

    def __init__(self):
        super().__init__()

        self._config_manager = get_config_manager()
        self._current_profile: Optional[GPUProfile] = None
        self._dark_mode = True

        # Load an NVIDIA profile by default
        self._load_default_profile()

        self._setup_window()
        self._setup_ui()
        self._create_menus()
        self._apply_theme()

    def _load_default_profile(self) -> None:
        """Load the first NVIDIA profile as default."""
        profiles = self._config_manager.list_profiles()
        for p in profiles:
            if p.is_nvidia:
                self._current_profile = p
                break
        if not self._current_profile and profiles:
            self._current_profile = profiles[0]

    def _setup_window(self) -> None:
        """Configure the main window."""
        self.setWindowTitle("NVIDIA Control Panel")
        self.setMinimumSize(900, 600)
        self.resize(1000, 700)

        # Try to load NVIDIA icon
        icon_paths = [
            project_root / "Agenda" / "512x512.png",
            project_root / "assets" / "icons" / "nvidia.ico",
        ]
        for path in icon_paths:
            if path.exists():
                self.setWindowIcon(QIcon(str(path)))
                break

    def _setup_ui(self) -> None:
        """Set up the main UI layout."""
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header with NVIDIA branding
        header = self._create_header()
        main_layout.addWidget(header)

        # Main content area with splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(1)

        # Left: Navigation tree
        nav_frame = QFrame()
        nav_layout = QVBoxLayout(nav_frame)
        nav_layout.setContentsMargins(10, 10, 5, 10)

        nav_label = QLabel("Select a Task...")
        nav_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        nav_layout.addWidget(nav_label)

        self._nav_tree = QTreeWidget()
        self._nav_tree.setHeaderHidden(True)
        self._nav_tree.setIndentation(15)
        self._nav_tree.currentItemChanged.connect(self._on_nav_changed)
        nav_layout.addWidget(self._nav_tree)

        splitter.addWidget(nav_frame)

        # Right: Content panels
        self._content_stack = QStackedWidget()

        # Create panels
        self._system_info_panel = SystemInfoPanel()
        self._manage_3d_panel = Manage3DPanel()
        self._display_panel = DisplaySettingsPanel()

        self._content_stack.addWidget(self._system_info_panel)  # 0
        self._content_stack.addWidget(self._manage_3d_panel)    # 1
        self._content_stack.addWidget(self._display_panel)      # 2

        # Set profile on panels
        if self._current_profile:
            self._system_info_panel.set_profile(self._current_profile)
            self._manage_3d_panel.set_profile(self._current_profile)
            self._display_panel.set_profile(self._current_profile)

        splitter.addWidget(self._content_stack)
        splitter.setSizes([250, 750])

        main_layout.addWidget(splitter)

        # Create navigation items
        self._create_navigation()

        # Status bar
        self._status_bar = QStatusBar()
        self.setStatusBar(self._status_bar)
        self._update_status()

    def _create_header(self) -> QWidget:
        """Create the NVIDIA branded header."""
        header = QFrame()
        header.setFixedHeight(60)
        header.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {NVIDIA_BLACK}, stop:0.5 {NVIDIA_GREEN}, stop:1 {NVIDIA_BLACK});
                border-bottom: 2px solid {NVIDIA_GREEN};
            }}
        """)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 5, 20, 5)

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
        title = QLabel("NVIDIA Control Panel")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet("color: white; margin-left: 10px;")
        layout.addWidget(title)

        layout.addStretch()

        # GPU info
        if self._current_profile:
            gpu_label = QLabel(self._current_profile.name)
            gpu_label.setStyleSheet("color: white; font-size: 12px;")
            layout.addWidget(gpu_label)

        return header

    def _create_navigation(self) -> None:
        """Create the navigation tree items."""
        # 3D Settings
        settings_3d = QTreeWidgetItem(["3D Settings"])
        manage_3d = QTreeWidgetItem(["Manage 3D settings"])
        manage_3d.setData(0, Qt.UserRole, 1)
        settings_3d.addChild(manage_3d)
        self._nav_tree.addTopLevelItem(settings_3d)

        # Display
        display = QTreeWidgetItem(["Display"])
        change_res = QTreeWidgetItem(["Change resolution"])
        change_res.setData(0, Qt.UserRole, 2)
        display.addChild(change_res)
        self._nav_tree.addTopLevelItem(display)

        # Video
        video = QTreeWidgetItem(["Video"])
        adjust_video = QTreeWidgetItem(["Adjust video color settings"])
        adjust_video.setData(0, Qt.UserRole, 2)
        video.addChild(adjust_video)
        self._nav_tree.addTopLevelItem(video)

        # Help
        help_item = QTreeWidgetItem(["Help"])
        sys_info = QTreeWidgetItem(["System Information"])
        sys_info.setData(0, Qt.UserRole, 0)
        help_item.addChild(sys_info)
        self._nav_tree.addTopLevelItem(help_item)

        # Expand all and select System Information
        self._nav_tree.expandAll()
        self._nav_tree.setCurrentItem(sys_info)

    def _create_menus(self) -> None:
        """Create the menu bar."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # View menu
        view_menu = menubar.addMenu("View")
        theme_action = QAction("Toggle Dark/Light Theme", self)
        theme_action.triggered.connect(self._toggle_theme)
        view_menu.addAction(theme_action)

        # Help menu
        help_menu = menubar.addMenu("Help")
        about_action = QAction("About...", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _apply_theme(self) -> None:
        """Apply the current theme."""
        self.setStyleSheet(get_theme(self._dark_mode))

    def _toggle_theme(self) -> None:
        """Toggle between dark and light themes."""
        self._dark_mode = not self._dark_mode
        self._apply_theme()

    def _on_nav_changed(self, current: QTreeWidgetItem, previous: QTreeWidgetItem) -> None:
        """Handle navigation selection change."""
        if current:
            panel_index = current.data(0, Qt.UserRole)
            if panel_index is not None:
                self._content_stack.setCurrentIndex(panel_index)

    def _update_status(self) -> None:
        """Update the status bar."""
        if self._current_profile:
            self._status_bar.showMessage(
                f"Driver Version: {self._current_profile.driver_version} | "
                f"GPU: {self._current_profile.name}"
            )
        else:
            self._status_bar.showMessage("No GPU profile loaded")

    def _show_about(self) -> None:
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About NVIDIA Control Panel",
            f"NVIDIA Control Panel\n\n"
            f"Version: {self._current_profile.driver_version if self._current_profile else '1.0.0'}\n\n"
            f"© 2024 NVIDIA Corporation"
        )


def main():
    """Main entry point."""
    app = QApplication(sys.argv)
    app.setApplicationName("NVIDIA Control Panel")

    window = NVIDIAControlPanel()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
