"""
Main Window
Enhanced GPU-SIM Control Panel with modular UI.
"""

import sys
import logging
from typing import Optional
from pathlib import Path

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTreeWidget, QTreeWidgetItem, QStackedWidget, QMenuBar, QMenu,
    QAction, QStatusBar, QSplitter, QMessageBox, QFileDialog
)
from PyQt5.QtGui import QIcon, QFont, QPainter, QPixmap, QColor
from PyQt5.QtCore import Qt, QTimer

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.config_manager import get_config_manager, ConfigManager
from src.core.gpu_profile import GPUProfile
from src.ui.widgets.gpu_selector import GPUSelector
from src.ui.panels.home_panel import HomePanel
from src.ui.panels.gpu_info_panel import GPUInfoPanel
from src.ui.panels.profile_editor import ProfileEditorPanel
from src.ui.panels.verification_panel import VerificationPanel
from src.ui.system_tray import SystemTrayManager
from src.ui.theme import Theme

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """
    Main GPU-SIM Control Panel window.
    Enhanced version with modular panels and working features.
    """

    def __init__(self):
        super().__init__()

        self._config_manager = get_config_manager()
        self._current_profile: Optional[GPUProfile] = None

        self._setup_window()
        self._create_menus()
        self._create_ui()
        self._create_status_bar()

        # Apply dark theme
        self._apply_dark_theme()

        logger.info("MainWindow initialized")

    def _setup_window(self) -> None:
        """Configure the main window."""
        self.setWindowTitle("GPU-SIM Control Panel")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(900, 600)

        # Try to set window icon
        icon_paths = [
            project_root / "assets" / "icons" / "gpu_sim.ico",
            Path("C:/Dell/Drivers/log/294666_nvidia_icon.ico"),
        ]
        for icon_path in icon_paths:
            if icon_path.exists():
                self.setWindowIcon(QIcon(str(icon_path)))
                break

    def _apply_dark_theme(self) -> None:
        """Apply a dark theme to the application."""
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {Theme.COLOR_BACKGROUND};
            }}
            QWidget {{
                background-color: {Theme.COLOR_SURFACE};
                color: {Theme.COLOR_TEXT_PRIMARY};
                font-family: '{Theme.FONT_FAMILY}', Arial, sans-serif;
                font-size: {Theme.FONT_BODY_SIZE}px;
            }}
            QTreeWidget {{
                background-color: {Theme.COLOR_SURFACE};
                border: none;
                color: {Theme.COLOR_TEXT_PRIMARY};
            }}
            QTreeWidget::item {{
                padding: 8px;
                border-radius: 4px;
            }}
            QTreeWidget::item:hover {{
                background-color: {Theme.COLOR_SURFACE_HOVER};
            }}
            QTreeWidget::item:selected {{
                background-color: {Theme.COLOR_ACCENT};
                color: white;
            }}
            QGroupBox {{
                font-weight: bold;
                border: 1px solid {Theme.COLOR_BORDER};
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: {Theme.COLOR_ACCENT};
            }}
            QComboBox {{
                background-color: {Theme.COLOR_BACKGROUND};
                border: 1px solid {Theme.COLOR_BORDER};
                border-radius: 3px;
                padding: 5px;
                min-width: 150px;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QPushButton {{
                background-color: {Theme.COLOR_SURFACE};
                color: {Theme.COLOR_TEXT_PRIMARY};
                border: 1px solid {Theme.COLOR_BORDER};
                padding: 8px 16px;
                border-radius: 3px;
            }}
            QPushButton:hover {{
                background-color: {Theme.COLOR_SURFACE_HOVER};
                border-color: {Theme.COLOR_ACCENT};
            }}
            QPushButton:pressed {{
                background-color: {Theme.COLOR_BACKGROUND};
            }}
            QPushButton:disabled {{
                background-color: {Theme.COLOR_SURFACE};
                color: {Theme.COLOR_TEXT_SECONDARY};
                border-color: {Theme.COLOR_BORDER};
            }}
            QMenuBar {{
                background-color: {Theme.COLOR_BACKGROUND};
                border-bottom: 1px solid {Theme.COLOR_BORDER};
            }}
            QMenuBar::item:selected {{
                background-color: {Theme.COLOR_ACCENT};
            }}
            QMenu {{
                background-color: {Theme.COLOR_SURFACE};
                border: 1px solid {Theme.COLOR_BORDER};
            }}
            QMenu::item:selected {{
                background-color: {Theme.COLOR_ACCENT};
            }}
            QStatusBar {{
                background-color: {Theme.COLOR_ACCENT};
                color: white;
            }}
            QTableWidget {{
                background-color: {Theme.COLOR_BACKGROUND};
                gridline-color: {Theme.COLOR_BORDER};
            }}
            QHeaderView::section {{
                background-color: {Theme.COLOR_SURFACE};
                padding: 5px;
                border: none;
            }}
            QCheckBox {{
                spacing: 8px;
            }}
            QSlider::groove:horizontal {{
                background-color: {Theme.COLOR_BACKGROUND};
                height: 8px;
                border-radius: 4px;
            }}
            QSlider::handle:horizontal {{
                background-color: {Theme.COLOR_ACCENT};
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }}
            QSpinBox {{
                background-color: {Theme.COLOR_BACKGROUND};
                border: 1px solid {Theme.COLOR_BORDER};
                padding: 5px;
            }}
        """)

    def _create_menus(self) -> None:
        """Create the menu bar."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")

        load_profile_action = QAction("Load Profile...", self)
        load_profile_action.triggered.connect(self._on_load_profile)
        file_menu.addAction(load_profile_action)

        save_profile_action = QAction("Save Profile As...", self)
        save_profile_action.triggered.connect(self._on_save_profile)
        file_menu.addAction(save_profile_action)

        file_menu.addSeparator()

        refresh_action = QAction("Refresh Profiles", self)
        refresh_action.setShortcut("F5")
        refresh_action.triggered.connect(self._refresh_profiles)
        file_menu.addAction(refresh_action)

        file_menu.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Alt+F4")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Tools menu
        tools_menu = menubar.addMenu("Tools")

        wmi_action = QAction("View WMI GPU Info", self)
        wmi_action.triggered.connect(self._show_wmi_info)
        tools_menu.addAction(wmi_action)

        registry_action = QAction("View Registry Info", self)
        registry_action.triggered.connect(self._show_registry_info)
        tools_menu.addAction(registry_action)

        tools_menu.addSeparator()

        backup_action = QAction("Create Registry Backup", self)
        backup_action.triggered.connect(self._create_backup)
        tools_menu.addAction(backup_action)

        # Help menu
        help_menu = menubar.addMenu("Help")

        about_action = QAction("About GPU-SIM", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

        docs_action = QAction("Documentation", self)
        docs_action.triggered.connect(self._show_docs)
        help_menu.addAction(docs_action)

    def _create_ui(self) -> None:
        """Create the main UI layout."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)

        # Left sidebar
        sidebar_widget = QWidget()
        sidebar_layout = QVBoxLayout(sidebar_widget)
        sidebar_layout.setContentsMargins(10, 10, 10, 10)

        # GPU Selector at top of sidebar
        self._gpu_selector = GPUSelector(self._config_manager)
        self._gpu_selector.profile_changed.connect(self._on_profile_changed)
        sidebar_layout.addWidget(self._gpu_selector)

        # Navigation tree
        self._nav_tree = QTreeWidget()
        self._nav_tree.setHeaderHidden(True)
        self._nav_tree.setIndentation(20)
        self._create_navigation()
        self._nav_tree.currentItemChanged.connect(self._on_nav_changed)
        sidebar_layout.addWidget(self._nav_tree)

        splitter.addWidget(sidebar_widget)

        # Right content area
        self._content_stack = QStackedWidget()

        # Create panels (simplified - only essential ones)
        self._home_panel = HomePanel()
        self._gpu_info_panel = GPUInfoPanel()
        self._profile_editor = ProfileEditorPanel()
        self._verification_panel = VerificationPanel()

        self._content_stack.addWidget(self._home_panel)     # Index 0
        self._content_stack.addWidget(self._gpu_info_panel) # Index 1
        self._content_stack.addWidget(self._profile_editor) # Index 2
        self._content_stack.addWidget(self._verification_panel) # Index 3

        # Connect profile editor updates to refresh all panels
        self._profile_editor.profile_updated.connect(self._on_profile_updated)

        splitter.addWidget(self._content_stack)

        # Set splitter sizes
        splitter.setSizes([280, 920])

        main_layout.addWidget(splitter)

    def _create_navigation(self) -> None:
        """Create the navigation tree (simplified)."""
        # Home
        home_item = QTreeWidgetItem(["Home"])
        home_item.setData(0, Qt.UserRole, 0)
        self._nav_tree.addTopLevelItem(home_item)

        # GPU Information
        gpu_info = QTreeWidgetItem(["GPU Information"])
        gpu_info.setData(0, Qt.UserRole, 1)
        self._nav_tree.addTopLevelItem(gpu_info)

        # Profile Editor
        editor = QTreeWidgetItem(["Profile Editor"])
        editor.setData(0, Qt.UserRole, 2)
        self._nav_tree.addTopLevelItem(editor)

        # Verification Checklist
        verification = QTreeWidgetItem(["Verification"])
        verification.setData(0, Qt.UserRole, 3)
        self._nav_tree.addTopLevelItem(verification)

        # Expand all and select home
        self._nav_tree.expandAll()
        self._nav_tree.setCurrentItem(home_item)

    def _create_status_bar(self) -> None:
        """Create the status bar."""
        self._status_bar = QStatusBar()
        self.setStatusBar(self._status_bar)
        self._update_status("Ready")

    def _update_status(self, message: str) -> None:
        """Update status bar message."""
        profile_text = ""
        if self._current_profile:
            profile_text = f" | Profile: {self._current_profile.name}"
        self._status_bar.showMessage(f"{message}{profile_text}")

    def _on_profile_changed(self, profile: Optional[GPUProfile]) -> None:
        """Handle GPU profile selection change."""
        self._current_profile = profile
        self._config_manager.active_profile = profile

        # Update all panels
        self._home_panel.set_profile(profile)
        self._gpu_info_panel.set_profile(profile)
        self._profile_editor.set_profile(profile)
        self._verification_panel.set_profile(profile)

        if profile:
            self._update_status(f"Selected: {profile.name}")
        else:
            self._update_status("No profile selected")

    def _on_profile_updated(self, updated_profile: GPUProfile) -> None:
        """Handle profile update from editor - refresh all panels with new data."""
        # Update local reference
        self._current_profile = updated_profile
        self._config_manager.active_profile = updated_profile

        # Refresh all panels with updated profile
        self._home_panel.set_profile(updated_profile)
        self._gpu_info_panel.set_profile(updated_profile)
        self._verification_panel.set_profile(updated_profile)
        # Don't update profile_editor - it triggered this

        # Refresh the GPU selector dropdown to show updated profile
        self._gpu_selector.refresh_profiles()

        self._update_status(f"Profile updated: {updated_profile.name}")

    def _on_nav_changed(self, current: QTreeWidgetItem, previous: QTreeWidgetItem) -> None:
        """Handle navigation tree selection change."""
        if current:
            panel_index = current.data(0, Qt.UserRole)
            if panel_index is not None:
                self._content_stack.setCurrentIndex(panel_index)

    def _refresh_profiles(self) -> None:
        """Refresh GPU profiles."""
        self._config_manager.load_profiles()
        self._update_status("Profiles refreshed")

    def _on_load_profile(self) -> None:
        """Load a profile from file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Load GPU Profile",
            str(self._config_manager.profiles_dir),
            "JSON Files (*.json)"
        )
        if file_path:
            self._refresh_profiles()
            self._update_status(f"Loaded profile from {file_path}")

    def _on_save_profile(self) -> None:
        """Save current profile to file."""
        if not self._current_profile:
            QMessageBox.warning(self, "No Profile", "No profile selected to save.")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save GPU Profile",
            str(self._config_manager.profiles_dir / f"{self._current_profile.id}.json"),
            "JSON Files (*.json)"
        )
        if file_path:
            self._config_manager.save_profile(self._current_profile, overwrite=True)
            self._update_status(f"Saved profile to {file_path}")

    def _show_wmi_info(self) -> None:
        """Show WMI GPU information."""
        self._home_panel._on_wmi_clicked()

    def _show_registry_info(self) -> None:
        """Show registry GPU information."""
        try:
            from src.registry.gpu_registry import get_gpu_registry

            registry = get_gpu_registry()
            info = registry.get_current_gpu_info()

            if info:
                text = "Current GPU from Registry:\n\n"
                for key, value in info.items():
                    text += f"{key}: {value}\n"
            else:
                text = "No GPU information found in registry."

            QMessageBox.information(self, "Registry GPU Info", text)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not query registry:\n\n{str(e)}")

    def _create_backup(self) -> None:
        """Create a registry backup."""
        try:
            from src.registry.backup_manager import get_backup_manager

            reply = QMessageBox.question(
                self,
                "Create Backup",
                "Create a backup of GPU-related registry entries?",
                QMessageBox.Yes | QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                backup_manager = get_backup_manager()
                backups = backup_manager.create_full_gpu_backup()

                if backups:
                    QMessageBox.information(
                        self,
                        "Backup Created",
                        f"Created {len(backups)} backup file(s) in:\n\n{backup_manager.backup_dir}"
                    )
                else:
                    QMessageBox.warning(self, "Backup Failed", "No backup files were created.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Backup failed:\n\n{str(e)}")

    def _show_about(self) -> None:
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About GPU-SIM",
            """<h2>GPU-SIM Control Panel</h2>
            <p>Version 1.0.0</p>
            <p>Virtual GPU Simulator for Windows</p>
            <hr>
            <p>This application allows you to simulate virtual GPU
            configurations that appear in Windows Task Manager,
            DxDiag, and system settings.</p>
            <p><b>⚠️ Warning:</b> Registry modifications can affect
            system stability. Always create backups first!</p>
            <hr>
            <p>© 2024 CodeDeX - GPU-SIM Project</p>
            """
        )

    def _show_docs(self) -> None:
        """Show documentation."""
        docs_path = project_root / "docs"
        QMessageBox.information(
            self,
            "Documentation",
            f"Documentation is available in:\n\n{docs_path}\n\n"
            f"• ARCHITECTURE.md - Project structure\n"
            f"• REGISTRY_REFERENCE.md - Registry details\n"
            f"• IDD_ROADMAP.md - Driver development guide"
        )


def main():
    """Application entry point."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    )

    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("GPU-SIM")
    app.setOrganizationName("CodeDeX")

    # Create and show main window
    window = MainWindow()
    window.show()

    # Run event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
