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


class StatCard(QFrame):
    """A card widget displaying a statistic."""

    def __init__(self, title: str, value: str, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Box | QFrame.Raised)
        self.setStyleSheet("""
            StatCard {
                background-color: #2d2d2d;
                border-radius: 8px;
                border: 1px solid #3d3d3d;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)

        self._title_label = QLabel(title)
        self._title_label.setStyleSheet("color: #888; font-size: 11px;")
        layout.addWidget(self._title_label)

        self._value_label = QLabel(value)
        self._value_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self._value_label.setStyleSheet("color: #76b900;")  # NVIDIA green
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
        header.setFont(QFont("Segoe UI", 24, QFont.Bold))
        header.setStyleSheet("color: #76b900;")  # NVIDIA green
        layout.addWidget(header)

        subtitle = QLabel("Virtual GPU Simulator for Windows")
        subtitle.setStyleSheet("color: #888; font-size: 14px;")
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
            QPushButton:disabled {
                background-color: #444;
                color: #888;
            }
        """)
        self._apply_btn.setEnabled(False)
        self._apply_btn.clicked.connect(self._on_apply_clicked)
        actions_layout.addWidget(self._apply_btn)

        self._wmi_btn = QPushButton("🔍 View WMI Info")
        self._wmi_btn.clicked.connect(self._on_wmi_clicked)
        actions_layout.addWidget(self._wmi_btn)

        # NVIDIA Control Panel button
        self._nvidia_btn = QPushButton("🟢 NVIDIA Control Panel")
        self._nvidia_btn.setStyleSheet("""
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
        self._nvidia_btn.clicked.connect(self._on_nvidia_panel_clicked)
        actions_layout.addWidget(self._nvidia_btn)

        # Installation Wizard button
        self._wizard_btn = QPushButton("🚀 Run Installation Wizard")
        self._wizard_btn.setStyleSheet("""
            QPushButton {
                background-color: #1976d2;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2196f3;
            }
        """)
        self._wizard_btn.clicked.connect(self._on_wizard_clicked)
        actions_layout.addWidget(self._wizard_btn)

        actions_layout.addStretch()
        layout.addLayout(actions_layout)

        # GPU-Z Bypass toggle (v2.0.0 feature)
        bypass_layout = QHBoxLayout()
        self._gpuz_bypass_checkbox = QCheckBox("🛡️ Enable GPU-Z Bypass (requires built DLL)")
        self._gpuz_bypass_checkbox.setStyleSheet("""
            QCheckBox {
                color: #888;
                font-size: 12px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:checked {
                background-color: #76b900;
                border: 2px solid #76b900;
                border-radius: 3px;
            }
            QCheckBox::indicator:unchecked {
                background-color: #333;
                border: 2px solid #555;
                border-radius: 3px;
            }
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
            footer = QLabel("✅ Running as Administrator - Full functionality enabled")
            footer.setStyleSheet("color: #76b900; font-size: 11px;")
        else:
            footer = QLabel("⚠️ Run as Administrator to apply changes to registry")
            footer.setStyleSheet("color: #f44336; font-size: 11px;")
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
                    label.setText(f"✅ {feature_name}")
                    label.setStyleSheet("color: #76b900;")
                else:
                    label.setText(f"❌ {feature_name}")
                    label.setStyleSheet("color: #666;")

            self._apply_btn.setEnabled(True)
        else:
            self._gpu_name_label.setText("No GPU Selected")
            self._gpu_manufacturer_label.setText("")
            self._vram_card.set_value("-- GB")
            self._cores_card.set_value("--")
            self._clock_card.set_value("-- MHz")
            self._driver_card.set_value("--")

            for label in self._feature_labels.values():
                label.setStyleSheet("color: #666;")

            self._apply_btn.setEnabled(False)

    def _on_apply_clicked(self) -> None:
        """Handle apply button click."""
        if not self._current_profile:
            return

        reply = QMessageBox.warning(
            self,
            "Apply GPU Profile",
            f"This will modify Windows registry to simulate:\n\n"
            f"{self._current_profile.name}\n\n"
            f"⚠️ This requires Administrator privileges!\n"
            f"⚠️ Create a backup first!\n\n"
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
        """Handle GPU-Z bypass toggle."""
        from pathlib import Path
        import shutil

        # Path to the built DLL
        project_root = Path(__file__).parent.parent.parent.parent
        dll_source = project_root / "injector" / "fakenvapi" / "build" / "nvapi64.dll"

        if checked:
            if not dll_source.exists():
                QMessageBox.warning(
                    self,
                    "DLL Not Found",
                    "GPU-Z bypass DLL not found!\n\n"
                    "Please build it first:\n"
                    "1. Open VS2022 Developer Command Prompt\n"
                    "2. cd injector/fakenvapi\n"
                    "3. meson setup build\n"
                    "4. meson compile -C build"
                )
                self._gpuz_bypass_checkbox.setChecked(False)
                return

            QMessageBox.information(
                self,
                "GPU-Z Bypass Enabled",
                "GPU-Z bypass is now active.\n\n"
                "Copy nvapi64.dll next to GPU-Z.exe to spoof GPU info.\n"
                f"DLL location: {dll_source}"
            )
        else:
            QMessageBox.information(
                self,
                "GPU-Z Bypass Disabled",
                "GPU-Z bypass has been disabled."
            )
