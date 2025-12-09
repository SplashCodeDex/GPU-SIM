"""
GPU-SIM Installer Wizard
A 5-step PyQt5 wizard for streamlined GPU simulation setup.
"""

import sys
import logging
from pathlib import Path
from typing import Optional

from PyQt5.QtWidgets import (
    QWizard, QWizardPage, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QCheckBox, QProgressBar, QGroupBox, QSpinBox,
    QPushButton, QTextEdit, QFrame, QMessageBox, QApplication
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal

# Ensure project root is in path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.config_manager import get_config_manager
from src.core.gpu_profile import GPUProfile

logger = logging.getLogger(__name__)


class WelcomePage(QWizardPage):
    """Step 1: Welcome and GPU Profile Selection."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Welcome to GPU-SIM Setup")
        self.setSubTitle("Configure your virtual GPU simulation in a few easy steps.")

        self._config_manager = get_config_manager()
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # Welcome message
        welcome_label = QLabel(
            "This wizard will help you:\n\n"
            "1. Select a GPU profile to simulate\n"
            "2. Configure VRAM and driver settings\n"
            "3. Install NVIDIA Control Panel and GeForce Experience\n"
            "4. Apply changes to your system\n\n"
            "⚠️ Administrator privileges are required for system modifications."
        )
        welcome_label.setWordWrap(True)
        welcome_label.setFont(QFont("Segoe UI", 10))
        layout.addWidget(welcome_label)

        layout.addSpacing(20)

        # GPU Profile Selection
        profile_group = QGroupBox("Select GPU Profile")
        profile_layout = QVBoxLayout(profile_group)

        self._profile_combo = QComboBox()
        self._profile_combo.setMinimumHeight(35)
        self._profile_combo.setFont(QFont("Segoe UI", 11))

        # Load profiles
        profiles = self._config_manager.list_profiles()
        for profile in profiles:
            display_text = f"{profile.name} ({profile.vram_gb:.0f} GB)"
            self._profile_combo.addItem(display_text, profile)

        # Default to first NVIDIA profile
        for i, profile in enumerate(profiles):
            if profile.is_nvidia:
                self._profile_combo.setCurrentIndex(i)
                break

        profile_layout.addWidget(self._profile_combo)

        # Profile info label
        self._info_label = QLabel()
        self._info_label.setStyleSheet("color: #76b900;")  # NVIDIA green
        self._profile_combo.currentIndexChanged.connect(self._update_info)
        self._update_info()
        profile_layout.addWidget(self._info_label)

        layout.addWidget(profile_group)
        layout.addStretch()

        # Register field for wizard access
        self.registerField("profileIndex", self._profile_combo)

    def _update_info(self):
        profile = self._profile_combo.currentData()
        if profile:
            info = (f"🎮 {profile.cuda_cores or profile.stream_processors or 0} "
                    f"{'CUDA Cores' if profile.is_nvidia else 'Stream Processors'} | "
                    f"📺 {profile.vram_gb:.0f} GB {profile.vram_type or 'GDDR'} | "
                    f"🔧 Driver {profile.driver_version}")
            self._info_label.setText(info)

    def get_selected_profile(self) -> Optional[GPUProfile]:
        """Return the currently selected GPU profile."""
        return self._profile_combo.currentData()


class ConfigPage(QWizardPage):
    """Step 2: Configuration Options."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Configure GPU Settings")
        self.setSubTitle("Customize VRAM and other settings (optional).")
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # VRAM Configuration
        vram_group = QGroupBox("Virtual VRAM")
        vram_layout = QHBoxLayout(vram_group)

        vram_layout.addWidget(QLabel("VRAM Size:"))
        self._vram_spin = QSpinBox()
        self._vram_spin.setRange(1, 48)
        self._vram_spin.setSuffix(" GB")
        self._vram_spin.setValue(4)
        self._vram_spin.setMinimumWidth(100)
        vram_layout.addWidget(self._vram_spin)

        # Quick VRAM buttons
        for gb in [4, 8, 12, 16, 24]:
            btn = QPushButton(f"{gb}GB")
            btn.setMaximumWidth(60)
            btn.clicked.connect(lambda checked, v=gb: self._vram_spin.setValue(v))
            vram_layout.addWidget(btn)

        vram_layout.addStretch()
        layout.addWidget(vram_group)

        # Driver Configuration
        driver_group = QGroupBox("Driver Settings")
        driver_layout = QVBoxLayout(driver_group)

        self._use_profile_driver = QCheckBox("Use profile's default driver version")
        self._use_profile_driver.setChecked(True)
        driver_layout.addWidget(self._use_profile_driver)

        layout.addWidget(driver_group)

        # Info box
        info_frame = QFrame()
        info_frame.setFrameStyle(QFrame.Box)
        info_layout = QVBoxLayout(info_frame)
        info_label = QLabel(
            "💡 Tip: Match the VRAM to what you want to show in Task Manager.\n"
            "Common choices: 4GB (GTX 780 Ti), 8GB (RTX 3070), 12GB (RTX 4070 Ti)"
        )
        info_label.setWordWrap(True)
        info_layout.addWidget(info_label)
        layout.addWidget(info_frame)

        layout.addStretch()

        # Register fields
        self.registerField("vramGB", self._vram_spin)
        self.registerField("useProfileDriver", self._use_profile_driver)

    def initializePage(self):
        """Called when page becomes visible - sync with selected profile."""
        wizard = self.wizard()
        if wizard and hasattr(wizard, 'get_selected_profile'):
            profile = wizard.get_selected_profile()
            if profile:
                self._vram_spin.setValue(int(profile.vram_gb))


class ComponentsPage(QWizardPage):
    """Step 3: Installation Component Selection."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Select Components to Install")
        self.setSubTitle("Choose which applications to install.")
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # Components
        components_group = QGroupBox("Components")
        comp_layout = QVBoxLayout(components_group)

        # Apply to Registry
        self._apply_registry = QCheckBox("Apply GPU profile to Windows Registry")
        self._apply_registry.setChecked(True)
        self._apply_registry.setToolTip("Modifies registry to spoof GPU in DxDiag and Settings")
        comp_layout.addWidget(self._apply_registry)

        # NVIDIA Control Panel
        self._install_panel = QCheckBox("Install NVIDIA Control Panel")
        self._install_panel.setChecked(True)
        self._install_panel.setToolTip("Installs fake NVIDIA Control Panel to Program Files")
        comp_layout.addWidget(self._install_panel)

        # GeForce Experience
        self._install_gfe = QCheckBox("Install GeForce Experience (optional)")
        self._install_gfe.setChecked(False)
        self._install_gfe.setToolTip("Installs fake GeForce Experience app")
        comp_layout.addWidget(self._install_gfe)

        layout.addWidget(components_group)

        # Warning
        warning_frame = QFrame()
        warning_frame.setStyleSheet("background-color: #3a3a00; border: 1px solid #666600;")
        warning_layout = QVBoxLayout(warning_frame)
        warning_label = QLabel(
            "⚠️ WARNING: Registry modifications require a restart to take full effect.\n"
            "A backup will be created automatically before any changes."
        )
        warning_label.setWordWrap(True)
        warning_label.setStyleSheet("color: #ffcc00;")
        warning_layout.addWidget(warning_label)
        layout.addWidget(warning_frame)

        layout.addStretch()

        # Register fields
        self.registerField("applyRegistry", self._apply_registry)
        self.registerField("installPanel", self._install_panel)
        self.registerField("installGFE", self._install_gfe)


class InstallWorker(QThread):
    """Background worker for installation tasks."""

    progress = pyqtSignal(int, str)  # percent, message
    finished = pyqtSignal(bool, str)  # success, message

    def __init__(self, profile: GPUProfile, vram_gb: int,
                 apply_registry: bool, install_panel: bool, install_gfe: bool):
        super().__init__()
        self._profile = profile
        self._vram_gb = vram_gb
        self._apply_registry = apply_registry
        self._install_panel = install_panel
        self._install_gfe = install_gfe
        self._errors = []

    def run(self):
        total_steps = sum([self._apply_registry, self._install_panel, self._install_gfe])
        if total_steps == 0:
            self.finished.emit(True, "No actions selected.")
            return

        current_step = 0

        try:
            # Step 1: Apply Registry
            if self._apply_registry:
                self.progress.emit(int(current_step / total_steps * 100),
                                   "Applying GPU profile to registry...")

                # Modify profile VRAM if changed
                if self._vram_gb != int(self._profile.vram_gb):
                    self._profile.vram_mb = self._vram_gb * 1024

                try:
                    from src.registry.gpu_registry import get_gpu_registry
                    registry = get_gpu_registry()
                    success = registry.apply_gpu_profile(self._profile)
                    if not success:
                        self._errors.append("Registry: Failed to apply (run as Administrator)")
                except Exception as e:
                    self._errors.append(f"Registry: {str(e)}")

                current_step += 1

            # Step 2: Install NVIDIA Control Panel
            if self._install_panel:
                self.progress.emit(int(current_step / total_steps * 100),
                                   "Installing NVIDIA Control Panel...")

                try:
                    from nvidia_panel.installer import install_nvidia_control_panel
                    nvidia_panel_dir = Path(__file__).parent.parent.parent / "nvidia_panel"
                    success, msg = install_nvidia_control_panel(nvidia_panel_dir)
                    if not success:
                        self._errors.append(f"NVIDIA Panel: {msg}")
                except Exception as e:
                    self._errors.append(f"NVIDIA Panel: {str(e)}")

                current_step += 1

            # Step 3: Install GeForce Experience
            if self._install_gfe:
                self.progress.emit(int(current_step / total_steps * 100),
                                   "Installing GeForce Experience...")

                try:
                    # Try to import GFE installer if it exists
                    from geforce_experience.gfe_installer import install_geforce_experience
                    gfe_dir = Path(__file__).parent.parent.parent / "geforce_experience"
                    success, msg = install_geforce_experience(gfe_dir)
                    if not success:
                        self._errors.append(f"GeForce Experience: {msg}")
                except ImportError:
                    # GFE installer not yet created - skip gracefully
                    self._errors.append("GeForce Experience: Installer not available yet")
                except Exception as e:
                    self._errors.append(f"GeForce Experience: {str(e)}")

                current_step += 1

            self.progress.emit(100, "Installation complete!")

            if self._errors:
                self.finished.emit(False, "Completed with errors:\n• " + "\n• ".join(self._errors))
            else:
                self.finished.emit(True, "All components installed successfully!")

        except Exception as e:
            self.finished.emit(False, f"Installation failed: {str(e)}")


class InstallPage(QWizardPage):
    """Step 4: Installation Progress."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Installing Components")
        self.setSubTitle("Please wait while components are being installed...")
        self._worker = None
        self._install_complete = False
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # Progress bar
        self._progress_bar = QProgressBar()
        self._progress_bar.setMinimum(0)
        self._progress_bar.setMaximum(100)
        self._progress_bar.setMinimumHeight(30)
        layout.addWidget(self._progress_bar)

        # Status label
        self._status_label = QLabel("Preparing installation...")
        self._status_label.setFont(QFont("Segoe UI", 10))
        layout.addWidget(self._status_label)

        # Log output
        self._log_text = QTextEdit()
        self._log_text.setReadOnly(True)
        self._log_text.setFont(QFont("Consolas", 9))
        self._log_text.setMaximumHeight(200)
        layout.addWidget(self._log_text)

        layout.addStretch()

    def initializePage(self):
        """Start installation when page becomes visible."""
        self._install_complete = False
        self._log_text.clear()
        self._progress_bar.setValue(0)

        wizard = self.wizard()
        if not wizard:
            return

        # Get configuration from wizard
        profile = wizard.get_selected_profile()
        if not profile:
            self._log_text.append("❌ No profile selected!")
            return

        vram_gb = self.field("vramGB")
        apply_registry = self.field("applyRegistry")
        install_panel = self.field("installPanel")
        install_gfe = self.field("installGFE")

        self._log_text.append(f"📦 Profile: {profile.name}")
        self._log_text.append(f"📺 VRAM: {vram_gb} GB")
        self._log_text.append(f"🔧 Apply Registry: {'Yes' if apply_registry else 'No'}")
        self._log_text.append(f"🖥️ Install NVIDIA Panel: {'Yes' if install_panel else 'No'}")
        self._log_text.append(f"🎮 Install GeForce Experience: {'Yes' if install_gfe else 'No'}")
        self._log_text.append("")

        # Create and start worker
        self._worker = InstallWorker(
            profile=profile,
            vram_gb=vram_gb,
            apply_registry=apply_registry,
            install_panel=install_panel,
            install_gfe=install_gfe
        )
        self._worker.progress.connect(self._on_progress)
        self._worker.finished.connect(self._on_finished)
        self._worker.start()

    def _on_progress(self, percent: int, message: str):
        self._progress_bar.setValue(percent)
        self._status_label.setText(message)
        self._log_text.append(f"▶ {message}")

    def _on_finished(self, success: bool, message: str):
        self._install_complete = True
        self._progress_bar.setValue(100)

        if success:
            self._status_label.setText("✅ " + message)
            self._log_text.append(f"\n✅ {message}")
        else:
            self._status_label.setText("⚠️ " + message.split('\n')[0])
            self._log_text.append(f"\n⚠️ {message}")

        # Enable next button
        self.completeChanged.emit()

    def isComplete(self):
        return self._install_complete


class CompletePage(QWizardPage):
    """Step 5: Completion and Next Steps."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Setup Complete!")
        self.setSubTitle("Your virtual GPU has been configured.")
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # Success message
        success_label = QLabel(
            "🎉 GPU-SIM setup is complete!\n\n"
            "Your system has been configured to simulate the selected GPU.\n"
            "Follow the verification steps below to confirm everything is working."
        )
        success_label.setWordWrap(True)
        success_label.setFont(QFont("Segoe UI", 11))
        layout.addWidget(success_label)

        layout.addSpacing(10)

        # Verification steps
        verify_group = QGroupBox("Verification Steps")
        verify_layout = QVBoxLayout(verify_group)

        steps = [
            ("1. Restart your computer", "Registry changes require a restart"),
            ("2. Open Task Manager", "Check Performance → GPU tab"),
            ("3. Run DxDiag", "Press Win+R, type 'dxdiag', check Display tab"),
            ("4. Open NVIDIA Control Panel", "From Start Menu or Desktop shortcut"),
            ("5. Check Windows Settings", "Settings → System → Display → Advanced"),
        ]

        for step, detail in steps:
            step_label = QLabel(f"<b>{step}</b><br><small>{detail}</small>")
            step_label.setTextFormat(Qt.RichText)
            verify_layout.addWidget(step_label)

        layout.addWidget(verify_group)

        # Quick launch buttons
        btn_layout = QHBoxLayout()

        self._dxdiag_btn = QPushButton("Run DxDiag")
        self._dxdiag_btn.clicked.connect(lambda: self._run_command("dxdiag"))
        btn_layout.addWidget(self._dxdiag_btn)

        self._taskmgr_btn = QPushButton("Open Task Manager")
        self._taskmgr_btn.clicked.connect(lambda: self._run_command("taskmgr"))
        btn_layout.addWidget(self._taskmgr_btn)

        layout.addLayout(btn_layout)
        layout.addStretch()

    def _run_command(self, cmd: str):
        import subprocess
        try:
            subprocess.Popen(cmd, shell=True)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to run {cmd}: {e}")


class InstallerWizard(QWizard):
    """Main installer wizard combining all pages."""

    def __init__(self, profile: Optional[GPUProfile] = None, parent=None):
        super().__init__(parent)
        self._initial_profile = profile

        self.setWindowTitle("GPU-SIM Setup Wizard")
        self.setWizardStyle(QWizard.ModernStyle)
        self.setMinimumSize(600, 500)

        # Apply dark theme
        self._apply_dark_theme()

        # Add pages
        self._welcome_page = WelcomePage()
        self._config_page = ConfigPage()
        self._components_page = ComponentsPage()
        self._install_page = InstallPage()
        self._complete_page = CompletePage()

        self.addPage(self._welcome_page)
        self.addPage(self._config_page)
        self.addPage(self._components_page)
        self.addPage(self._install_page)
        self.addPage(self._complete_page)

        # Set initial profile if provided
        if profile:
            # Find and select the matching profile in combo
            combo = self._welcome_page._profile_combo
            for i in range(combo.count()):
                if combo.itemData(i) and combo.itemData(i).id == profile.id:
                    combo.setCurrentIndex(i)
                    break

    def _apply_dark_theme(self):
        self.setStyleSheet("""
            QWizard {
                background-color: #1e1e1e;
            }
            QWizardPage {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
            }
            QGroupBox {
                color: #76b900;
                border: 1px solid #3a3a3a;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QComboBox, QSpinBox {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #3a3a3a;
                border-radius: 3px;
                padding: 5px;
            }
            QComboBox:hover, QSpinBox:hover {
                border: 1px solid #76b900;
            }
            QCheckBox {
                color: #ffffff;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QPushButton {
                background-color: #76b900;
                color: #000000;
                border: none;
                border-radius: 3px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #8bc34a;
            }
            QPushButton:pressed {
                background-color: #5a8f00;
            }
            QProgressBar {
                border: 1px solid #3a3a3a;
                border-radius: 3px;
                text-align: center;
                color: #ffffff;
            }
            QProgressBar::chunk {
                background-color: #76b900;
            }
            QTextEdit {
                background-color: #0d0d0d;
                color: #ffffff;
                border: 1px solid #3a3a3a;
            }
        """)

    def get_selected_profile(self) -> Optional[GPUProfile]:
        """Return the currently selected GPU profile from welcome page."""
        return self._welcome_page.get_selected_profile()


def main():
    """Test the installer wizard standalone."""
    app = QApplication(sys.argv)
    wizard = InstallerWizard()
    wizard.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
