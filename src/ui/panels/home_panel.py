"""
Home Panel
The main dashboard panel showing current GPU configuration.
"""

from typing import Optional
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QGroupBox, QGridLayout, QPushButton, QMessageBox, QCheckBox
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt

import sys
sys.path.insert(0, str(__file__).rsplit('src', 1)[0])

from src.core.gpu_profile import GPUProfile
from src.ui.theme import Theme


class StatCard(QFrame):
    """A card widget displaying a statistic."""

    def __init__(self, title: str, value: str, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Box | QFrame.Raised)
        self.setStyleSheet(f"""
            StatCard {{
                background-color: {Theme.COLOR_SURFACE};
                border-radius: 8px;
                border: 1px solid {Theme.COLOR_BORDER};
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)

        self._title_label = QLabel(title)
        self._title_label.setStyleSheet(f"color: {Theme.COLOR_TEXT_SECONDARY}; font-size: {Theme.FONT_SMALL_SIZE}px;")
        layout.addWidget(self._title_label)

        self._value_label = QLabel(value)
        self._value_label.setFont(QFont(Theme.FONT_FAMILY, 16, QFont.Bold))
        self._value_label.setStyleSheet(f"color: {Theme.COLOR_ACCENT};")
        layout.addWidget(self._value_label)

    def set_value(self, value: str) -> None:
        self._value_label.setText(value)

    def set_title(self, title: str) -> None:
        self._title_label.setText(title)


class HomePanel(QWidget):
    """
    Main dashboard panel showing virtual GPU information.
    """

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._current_profile: Optional[GPUProfile] = None
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the panel UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Header
        header = QLabel("GPU-SIM Control Panel")
        header.setFont(QFont(Theme.FONT_FAMILY, Theme.FONT_HEADER_SIZE, QFont.Bold))
        header.setStyleSheet(f"color: {Theme.COLOR_ACCENT};")
        layout.addWidget(header)

        subtitle = QLabel("Virtual GPU Simulator for Windows")
        subtitle.setStyleSheet(f"color: {Theme.COLOR_TEXT_SECONDARY}; font-size: {Theme.FONT_BODY_SIZE}px;")
        layout.addWidget(subtitle)

        layout.addSpacing(10)

        # Current GPU Section
        gpu_group = QGroupBox("Current Virtual GPU")
        gpu_layout = QVBoxLayout(gpu_group)

        self._gpu_name_label = QLabel("No GPU Selected")
        self._gpu_name_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        gpu_layout.addWidget(self._gpu_name_label)

        self._gpu_manufacturer_label = QLabel("")
        self._gpu_manufacturer_label.setStyleSheet("color: #888;")
        gpu_layout.addWidget(self._gpu_manufacturer_label)

        layout.addWidget(gpu_group)

        # Stats Cards
        stats_layout = QHBoxLayout()

        self._vram_card = StatCard("VRAM", "-- GB")
        stats_layout.addWidget(self._vram_card)

        self._cores_card = StatCard("Compute Units", "--")
        stats_layout.addWidget(self._cores_card)

        self._clock_card = StatCard("Boost Clock", "-- MHz")
        stats_layout.addWidget(self._clock_card)

        self._driver_card = StatCard("Driver Version", "--")
        stats_layout.addWidget(self._driver_card)

        layout.addLayout(stats_layout)

        # Features Section
        features_group = QGroupBox("Features")
        features_layout = QGridLayout(features_group)

        self._feature_labels = {}
        features = ["Ray Tracing", "DLSS/FSR", "CUDA/OpenCL", "NVENC/VCE"]
        for i, feature in enumerate(features):
            label = QLabel(f"❌ {feature}")
            label.setStyleSheet("color: #666;")
            self._feature_labels[feature] = label
            features_layout.addWidget(label, i // 2, i % 2)

        layout.addWidget(features_group)

        # Actions
        actions_layout = QHBoxLayout()

        self._apply_btn = QPushButton("⚡ Apply to System")
        self._apply_btn.setStyleSheet("""
            QPushButton {
                background-color: #76b900;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #8bc34a;
            }
        """)
        self._apply_btn.setEnabled(False)
        self._apply_btn.setStyleSheet(Theme.STYLE_BUTTON_PRIMARY)
        self._apply_btn.clicked.connect(self._on_apply_clicked)
        actions_layout.addWidget(self._apply_btn)

        self._wmi_btn = QPushButton("View WMI Info")
        self._wmi_btn.setStyleSheet(Theme.STYLE_BUTTON_SECONDARY)
        self._wmi_btn.clicked.connect(self._on_wmi_clicked)
        actions_layout.addWidget(self._wmi_btn)

        # NVIDIA Control Panel button
        self._nvidia_btn = QPushButton("NVIDIA Control Panel")
        self._nvidia_btn.setStyleSheet(Theme.STYLE_BUTTON_SECONDARY)
        self._nvidia_btn.clicked.connect(self._on_nvidia_panel_clicked)
        actions_layout.addWidget(self._nvidia_btn)

        # Install VDD (Virtual Display Driver) button
        self._vdd_btn = QPushButton("Install Virtual Display")
        # Override color to Purple for VDD to distinguish it, or use Primary.
        # Professional UI suggests consistency, let's use Primary (Green) or maybe a dedicated color?
        # Let's use Theme.STYLE_BUTTON_PRIMARY but maybe with a slightly different text to differentiate.
        # Actually, let's just use PRIMARY.
        self._vdd_btn.setStyleSheet(Theme.STYLE_BUTTON_PRIMARY)
        self._vdd_btn.setEnabled(False)
        self._vdd_btn.clicked.connect(self._on_vdd_install_clicked)
        actions_layout.addWidget(self._vdd_btn)

        # Installation Wizard button
        self._wizard_btn = QPushButton("Installation Wizard")
        self._wizard_btn.setStyleSheet(Theme.STYLE_BUTTON_SECONDARY)
        self._wizard_btn.clicked.connect(self._on_wizard_clicked)
        actions_layout.addWidget(self._wizard_btn)

        actions_layout.addStretch()
        layout.addLayout(actions_layout)

        # GPU-Z Bypass toggle
        bypass_layout = QHBoxLayout()
        self._gpuz_bypass_checkbox = QCheckBox("Enable GPU-Z Bypass")
        self._gpuz_bypass_checkbox.setStyleSheet(f"""
            QCheckBox {{
                color: {Theme.COLOR_TEXT_SECONDARY};
                font-size: 12px;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border: 2px solid {Theme.COLOR_BORDER};
                border-radius: 3px;
                background-color: {Theme.COLOR_SURFACE};
            }}
            QCheckBox::indicator:checked {{
                background-color: {Theme.COLOR_ACCENT};
                border-color: {Theme.COLOR_ACCENT};
            }}
        """)
        self._gpuz_bypass_checkbox.setToolTip(
            "When enabled, copies nvapi64.dll to intercept GPU-Z/HWiNFO queries.\n"
            "Requires building the DLL from injector/fakenvapi/"
        )
        self._gpuz_bypass_checkbox.toggled.connect(self._on_gpuz_bypass_toggled)
        bypass_layout.addWidget(self._gpuz_bypass_checkbox)
        bypass_layout.addStretch()
        layout.addLayout(bypass_layout)

        layout.addStretch()

        # Footer - show admin status
        import ctypes
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        except Exception:
            is_admin = False

        if is_admin:
            footer = QLabel("Admin Mode Active - Full Functionality")
            footer.setStyleSheet(f"color: {Theme.COLOR_ACCENT}; font-size: {Theme.FONT_SMALL_SIZE}px;")
        else:
            footer = QLabel("Restricted Mode - Run as Administrator Required")
            footer.setStyleSheet(f"color: {Theme.COLOR_DANGER}; font-size: {Theme.FONT_SMALL_SIZE}px;")
        layout.addWidget(footer)

    def set_profile(self, profile: Optional[GPUProfile]) -> None:
        """Update the panel with a new profile."""
        self._current_profile = profile

        if profile:
            self._gpu_name_label.setText(profile.name)
            self._gpu_manufacturer_label.setText(profile.manufacturer)

            self._vram_card.set_value(f"{profile.vram_gb:.0f} GB")

            cores = profile.cuda_cores or profile.stream_processors
            core_type = "CUDA" if profile.is_nvidia else "SP"
            self._cores_card.set_value(f"{cores} {core_type}")
            self._cores_card.set_title("CUDA Cores" if profile.is_nvidia else "Stream Processors")

            self._clock_card.set_value(f"{profile.boost_clock_mhz} MHz")
            self._driver_card.set_value(profile.driver_version)

            # Update features
            features = profile.features
            for feature_name, label in self._feature_labels.items():
                # Check various feature flags
                enabled = False
                if "Ray Tracing" in feature_name:
                    enabled = features.get("ray_tracing", False)
                elif "DLSS" in feature_name:
                    enabled = features.get("dlss", False) or features.get("fsr", False)
                elif "CUDA" in feature_name:
                    enabled = features.get("cuda", False) or profile.cuda_cores > 0
                elif "NVENC" in feature_name:
                    enabled = features.get("nvenc", False) or features.get("vce", False)

                if enabled:
                    label.setText(f"{feature_name}")
                    label.setStyleSheet(f"color: {Theme.COLOR_ACCENT}; font-weight: bold;")
                else:
                    label.setText(f"{feature_name}")
                    label.setStyleSheet(f"color: {Theme.COLOR_TEXT_SECONDARY}; text-decoration: line-through;")

            self._apply_btn.setEnabled(True)
            self._vdd_btn.setEnabled(True)
        else:
            self._gpu_name_label.setText("No GPU Selected")
            self._gpu_manufacturer_label.setText("")
            self._vram_card.set_value("-- GB")
            self._cores_card.set_value("--")
            self._clock_card.set_value("-- MHz")
            self._driver_card.set_value("--")

            for label in self._feature_labels.values():
                label.setStyleSheet(f"color: {Theme.COLOR_TEXT_SECONDARY};")

            self._apply_btn.setEnabled(False)
            self._vdd_btn.setEnabled(False)

    def _on_apply_clicked(self) -> None:
        """Handle apply button click."""
        if not self._current_profile:
            return

        reply = QMessageBox.warning(
            self,
            "Apply GPU Profile",
            f"This will modify Windows registry to simulate:\n\n"
            f"{self._current_profile.name}\n\n"
            f"Requires Administrator privileges.\n"
            f"Create a backup first.\n\n"
            f"Continue?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                from src.registry.gpu_registry import get_gpu_registry
                registry = get_gpu_registry()
                success = registry.apply_gpu_profile(self._current_profile)

                if success:
                    QMessageBox.information(
                        self,
                        "Success",
                        "GPU profile applied!\n\n"
                        "Restart your computer for changes to take effect."
                    )
                else:
                    QMessageBox.critical(
                        self,
                        "Error",
                        "Failed to apply GPU profile.\n\n"
                        "Make sure you're running as Administrator."
                    )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Error applying profile:\n\n{str(e)}"
                )

    def _on_vdd_install_clicked(self) -> None:
        """Handle VDD install button - one-click driver installation."""
        if not self._current_profile:
            return

        reply = QMessageBox.warning(
            self,
            "Install Virtual Display Driver",
            f"This will install a Virtual Display Driver that shows:\n\n"
            f"GPU: {self._current_profile.name}\n"
            f"VRAM: {int(self._current_profile.vram_gb * 1024)} MB\n\n"
            f"Requires Administrator privileges.\n"
            f"Requires Test Signing Mode enabled.\n\n"
            f"The driver will appear in DxDiag and Task Manager.\n\n"
            f"Continue?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                from src.vdd.vdd_installer import VDDInstaller, is_admin, is_test_signing_enabled

                if not is_admin():
                    QMessageBox.critical(
                        self,
                        "Administrator Required",
                        "Please run GPU-SIM as Administrator to install the driver."
                    )
                    return

                if not is_test_signing_enabled():
                    reply = QMessageBox.question(
                        self,
                        "Test Signing Required",
                        "Test signing mode is not enabled.\n\n"
                        "Would you like to enable it now?\n"
                        "(Requires a system reboot)",
                        QMessageBox.Yes | QMessageBox.No
                    )
                    if reply == QMessageBox.Yes:
                        from src.vdd.vdd_installer import enable_test_signing
                        if enable_test_signing():
                            QMessageBox.information(
                                self,
                                "Test Signing Enabled",
                                "Test signing has been enabled.\n\n"
                                "Please restart your computer, then run GPU-SIM again "
                                "to complete the VDD installation."
                            )
                        else:
                            QMessageBox.critical(
                                self,
                                "Error",
                                "Failed to enable test signing mode."
                            )
                    return

                # Calculate VRAM in MB
                vram_mb = int(self._current_profile.vram_gb * 1024)

                # Create and run installer
                installer = VDDInstaller(
                    gpu_name=self._current_profile.name,
                    manufacturer=self._current_profile.manufacturer
                )

                QMessageBox.information(
                    self,
                    "Installing...",
                    "Installing Virtual Display Driver...\n\n"
                    "This may take a moment. Click OK to proceed."
                )

                success = installer.full_install(vram_mb=vram_mb)

                if success:
                    QMessageBox.information(
                        self,
                        "Installation Complete",
                        f"Virtual Display Driver installed successfully!\n\n"
                        f"GPU: {self._current_profile.name}\n"
                        f"VRAM: {vram_mb} MB (shown in Chip Type field)\n\n"
                        f"The driver will persist across reboots via startup task.\n\n"
                        f"Check DxDiag → Display 2 to see the result."
                    )
                else:
                    QMessageBox.critical(
                        self,
                        "Installation Failed",
                        "Failed to install Virtual Display Driver.\n\n"
                        "Check the console output for details."
                    )

            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Error installing VDD:\n\n{str(e)}"
                )

    def _on_wmi_clicked(self) -> None:
        """Handle WMI info button click."""
        try:
            from src.wmi.wmi_monitor import get_wmi_monitor

            monitor = get_wmi_monitor()
            controllers = monitor.get_video_controllers()

            if not controllers:
                QMessageBox.information(
                    self,
                    "WMI GPU Info",
                    "No video controllers found via WMI."
                )
                return

            info_text = "Current GPU(s) as seen by Windows:\n\n"
            for i, ctrl in enumerate(controllers, 1):
                info_text += f"[GPU {i}] {ctrl.name}\n"
                info_text += f"  VRAM: {ctrl.adapter_ram_mb:.0f} MB\n"
                info_text += f"  Driver: {ctrl.driver_version}\n"
                info_text += f"  Status: {ctrl.status}\n\n"

            QMessageBox.information(self, "WMI GPU Info", info_text)

        except Exception as e:
            QMessageBox.warning(
                self,
                "WMI Error",
                f"Could not query WMI:\n\n{str(e)}\n\n"
                f"Make sure WMI module is installed:\npip install WMI"
            )

    def _on_nvidia_panel_clicked(self) -> None:
        """Install the NVIDIA Control Panel as a system app."""
        try:
            from nvidia_panel.installer import (
                install_nvidia_control_panel, is_installed, is_admin
            )
            from pathlib import Path

            # Check if already installed
            if is_installed():
                reply = QMessageBox.question(
                    self,
                    "NVIDIA Control Panel",
                    "NVIDIA Control Panel is already installed!\n\n"
                    "Would you like to reinstall it?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                if reply != QMessageBox.Yes:
                    return

            # Check admin privileges
            if not is_admin():
                QMessageBox.warning(
                    self,
                    "Administrator Required",
                    "Installing NVIDIA Control Panel requires Administrator privileges.\n\n"
                    "Please restart GPU-SIM as Administrator."
                )
                return

            # Get nvidia_panel source directory
            source_dir = Path(__file__).parent.parent.parent / "nvidia_panel"

            # Perform installation
            success, message = install_nvidia_control_panel(source_dir)

            if success:
                QMessageBox.information(
                    self,
                    "Installation Complete",
                    message
                )
            else:
                QMessageBox.critical(
                    self,
                    "Installation Failed",
                    message
                )

        except Exception as e:
            QMessageBox.warning(
                self,
                "Error",
                f"Could not install NVIDIA Control Panel:\n\n{str(e)}"
            )

    def _on_wizard_clicked(self) -> None:
        """Open the installation wizard."""
        try:
            from src.ui.installer_wizard import InstallerWizard

            wizard = InstallerWizard(profile=self._current_profile, parent=self)
            wizard.exec_()

        except Exception as e:
            QMessageBox.warning(
                self,
                "Error",
                f"Could not open installation wizard:\n\n{str(e)}"
            )

    def _on_gpuz_bypass_toggled(self, checked: bool) -> None:
        """Handle GPU-Z bypass toggle - auto-copies nvapi64.dll to known app folders."""
        from pathlib import Path
        import shutil
        import os

        # Path to the built DLL
        project_root = Path(__file__).parent.parent.parent.parent
        dll_source = project_root / "injector" / "fakenvapi" / "build" / "src" / "nvapi64.dll"

        # Common installation paths for GPU monitoring tools
        target_folders = [
            Path(os.environ.get('PROGRAMFILES(X86)', 'C:\\Program Files (x86)')) / "GPU-Z",
            Path(os.environ.get('PROGRAMFILES', 'C:\\Program Files')) / "GPU-Z",
            Path(os.environ.get('LOCALAPPDATA', '')) / "Programs" / "GPU-Z",
            Path(os.environ.get('PROGRAMFILES(X86)', 'C:\\Program Files (x86)')) / "CPUID" / "HWMonitor",
            Path(os.environ.get('PROGRAMFILES', 'C:\\Program Files')) / "HWINFO64",
            Path(os.environ.get('PROGRAMFILES(X86)', 'C:\\Program Files (x86)')) / "FinalWire" / "AIDA64 Extreme",
        ]

        if checked:
            if not dll_source.exists():
                QMessageBox.warning(
                    self,
                    "DLL Not Found",
                    "GPU-Z bypass DLL not found!\n\n"
                    f"Expected location:\n{dll_source}\n\n"
                    "Please build it first using VS2022 Developer Command Prompt:\n"
                    "cd injector/fakenvapi && meson setup build && ninja -C build"
                )
                self._gpuz_bypass_checkbox.setChecked(False)
                return

            # Copy to all found target folders
            copied_to = []
            for folder in target_folders:
                if folder.exists():
                    try:
                        target = folder / "nvapi64.dll"
                        shutil.copy2(dll_source, target)
                        copied_to.append(str(folder))
                    except PermissionError:
                        pass  # Skip folders we can't write to
                    except Exception:
                        pass

            if copied_to:
                QMessageBox.information(
                    self,
                    "GPU-Z Bypass Enabled",
                    f"nvapi64.dll copied to {len(copied_to)} location(s):\n\n" +
                    "\n".join(f"• {p}" for p in copied_to) +
                    "\n\nRestart GPU-Z/HWiNFO to see spoofed GPU info."
                )
            else:
                # No folders found, show manual copy instructions
                QMessageBox.information(
                    self,
                    "GPU-Z Bypass Enabled",
                    "GPU-Z/HWiNFO not found in default locations.\n\n"
                    "Manually copy nvapi64.dll to your GPU-Z folder:\n"
                    f"{dll_source}"
                )
        else:
            # Remove the DLL from target folders
            removed_from = []
            for folder in target_folders:
                target = folder / "nvapi64.dll"
                if target.exists():
                    try:
                        target.unlink()
                        removed_from.append(str(folder))
                    except Exception:
                        pass

            if removed_from:
                QMessageBox.information(
                    self,
                    "GPU-Z Bypass Disabled",
                    f"nvapi64.dll removed from {len(removed_from)} location(s).\n\n"
                    "Restart GPU-Z/HWiNFO to see original GPU info."
                )
            else:
                QMessageBox.information(
                    self,
                    "GPU-Z Bypass Disabled",
                    "GPU-Z bypass has been disabled."
                )
