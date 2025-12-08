"""
Profile Editor Panel
Allows editing GPU profile settings including VRAM, clocks, and other specs.
"""

from typing import Optional
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox,
    QPushButton, QLineEdit, QSpinBox, QComboBox, QFormLayout,
    QMessageBox, QScrollArea, QFrame
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.core.gpu_profile import GPUProfile
from src.core.config_manager import get_config_manager


class ProfileEditorPanel(QWidget):
    """
    Panel for editing GPU profile specifications.
    Allows customization of VRAM, clocks, and other settings.
    """

    profile_updated = pyqtSignal(object)  # Emits updated GPUProfile

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._current_profile: Optional[GPUProfile] = None
        self._config_manager = get_config_manager()
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the panel UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header
        header = QLabel("✏️ Profile Editor")
        header.setFont(QFont("Segoe UI", 18, QFont.Bold))
        layout.addWidget(header)

        subtitle = QLabel("Customize GPU specifications including VRAM size")
        subtitle.setStyleSheet("color: #888;")
        layout.addWidget(subtitle)

        # Scroll area for form
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)

        # Basic Info
        basic_group = QGroupBox("Basic Information")
        basic_form = QFormLayout(basic_group)

        self._name_edit = QLineEdit()
        self._name_edit.setPlaceholderText("GPU Name")
        basic_form.addRow("Name:", self._name_edit)

        self._manufacturer_combo = QComboBox()
        self._manufacturer_combo.addItems([
            "NVIDIA Corporation",
            "Advanced Micro Devices, Inc.",
            "Intel Corporation"
        ])
        basic_form.addRow("Manufacturer:", self._manufacturer_combo)

        self._driver_version = QLineEdit()
        self._driver_version.setPlaceholderText("e.g., 546.65")
        basic_form.addRow("Driver Version:", self._driver_version)

        form_layout.addWidget(basic_group)

        # Memory Settings (VRAM)
        memory_group = QGroupBox("⭐ Memory Settings")
        memory_form = QFormLayout(memory_group)

        # VRAM Size - this is the key customizable field
        vram_layout = QHBoxLayout()
        self._vram_spinbox = QSpinBox()
        self._vram_spinbox.setRange(512, 131072)  # 512MB to 128GB
        self._vram_spinbox.setSingleStep(1024)
        self._vram_spinbox.setSuffix(" MB")
        self._vram_spinbox.setValue(8192)
        vram_layout.addWidget(self._vram_spinbox)

        # Quick VRAM buttons
        for gb in [4, 8, 12, 16, 24, 32]:
            btn = QPushButton(f"{gb}GB")
            btn.setMaximumWidth(50)
            btn.clicked.connect(lambda checked, v=gb*1024: self._vram_spinbox.setValue(v))
            vram_layout.addWidget(btn)

        memory_form.addRow("VRAM Size:", vram_layout)

        self._vram_type_combo = QComboBox()
        self._vram_type_combo.addItems(["GDDR6X", "GDDR6", "GDDR5X", "GDDR5", "HBM2", "HBM2e", "HBM3"])
        memory_form.addRow("VRAM Type:", self._vram_type_combo)

        self._memory_bus = QSpinBox()
        self._memory_bus.setRange(64, 512)
        self._memory_bus.setSingleStep(32)
        self._memory_bus.setSuffix(" bit")
        self._memory_bus.setValue(256)
        memory_form.addRow("Memory Bus:", self._memory_bus)

        form_layout.addWidget(memory_group)

        # Clock Settings
        clock_group = QGroupBox("Clock Speeds")
        clock_form = QFormLayout(clock_group)

        self._base_clock = QSpinBox()
        self._base_clock.setRange(100, 5000)
        self._base_clock.setSuffix(" MHz")
        self._base_clock.setValue(1500)
        clock_form.addRow("Base Clock:", self._base_clock)

        self._boost_clock = QSpinBox()
        self._boost_clock.setRange(100, 5000)
        self._boost_clock.setSuffix(" MHz")
        self._boost_clock.setValue(1800)
        clock_form.addRow("Boost Clock:", self._boost_clock)

        self._memory_clock = QSpinBox()
        self._memory_clock.setRange(1000, 30000)
        self._memory_clock.setSuffix(" MHz")
        self._memory_clock.setValue(14000)
        clock_form.addRow("Memory Clock:", self._memory_clock)

        form_layout.addWidget(clock_group)

        # Processor Settings
        proc_group = QGroupBox("Processor")
        proc_form = QFormLayout(proc_group)

        self._cuda_cores = QSpinBox()
        self._cuda_cores.setRange(0, 50000)
        self._cuda_cores.setValue(0)
        proc_form.addRow("CUDA Cores:", self._cuda_cores)

        self._stream_processors = QSpinBox()
        self._stream_processors.setRange(0, 50000)
        self._stream_processors.setValue(0)
        proc_form.addRow("Stream Processors:", self._stream_processors)

        self._tdp = QSpinBox()
        self._tdp.setRange(35, 1000)
        self._tdp.setSuffix(" W")
        self._tdp.setValue(250)
        proc_form.addRow("TDP:", self._tdp)

        form_layout.addWidget(proc_group)

        form_layout.addStretch()

        scroll.setWidget(form_widget)
        layout.addWidget(scroll)

        # Action buttons
        btn_layout = QHBoxLayout()

        self._save_btn = QPushButton("💾 Save Changes")
        self._save_btn.clicked.connect(self._save_profile)
        self._save_btn.setEnabled(False)
        btn_layout.addWidget(self._save_btn)

        self._save_as_btn = QPushButton("📋 Save As New")
        self._save_as_btn.clicked.connect(self._save_as_new)
        self._save_as_btn.setEnabled(False)
        btn_layout.addWidget(self._save_as_btn)

        self._reset_btn = QPushButton("↩️ Reset")
        self._reset_btn.clicked.connect(self._reset_form)
        btn_layout.addWidget(self._reset_btn)

        layout.addLayout(btn_layout)

    def _update_form_from_profile(self, profile: GPUProfile) -> None:
        """Populate form fields from profile."""
        self._name_edit.setText(profile.name)

        # Set manufacturer
        idx = self._manufacturer_combo.findText(profile.manufacturer)
        if idx >= 0:
            self._manufacturer_combo.setCurrentIndex(idx)

        self._driver_version.setText(profile.driver_version)

        # Memory
        self._vram_spinbox.setValue(profile.vram_mb)
        idx = self._vram_type_combo.findText(profile.vram_type)
        if idx >= 0:
            self._vram_type_combo.setCurrentIndex(idx)
        self._memory_bus.setValue(profile.memory_bus_width)

        # Clocks
        self._base_clock.setValue(profile.base_clock_mhz)
        self._boost_clock.setValue(profile.boost_clock_mhz)
        self._memory_clock.setValue(profile.memory_clock_mhz)

        # Processor
        self._cuda_cores.setValue(profile.cuda_cores)
        self._stream_processors.setValue(profile.stream_processors)
        self._tdp.setValue(profile.tdp_watts)

        self._save_btn.setEnabled(True)
        self._save_as_btn.setEnabled(True)

    def _get_profile_from_form(self) -> Optional[GPUProfile]:
        """Create a GPUProfile from form fields."""
        if not self._current_profile:
            return None

        # Create updated profile with form values
        return GPUProfile(
            id=self._current_profile.id,
            name=self._name_edit.text() or self._current_profile.name,
            manufacturer=self._manufacturer_combo.currentText(),
            driver_version=self._driver_version.text() or "1.0.0",
            driver_date=self._current_profile.driver_date,
            vram_mb=self._vram_spinbox.value(),
            vram_type=self._vram_type_combo.currentText(),
            memory_bus_width=self._memory_bus.value(),
            base_clock_mhz=self._base_clock.value(),
            boost_clock_mhz=self._boost_clock.value(),
            memory_clock_mhz=self._memory_clock.value(),
            cuda_cores=self._cuda_cores.value(),
            stream_processors=self._stream_processors.value(),
            tdp_watts=self._tdp.value(),
            pci_device_id=self._current_profile.pci_device_id,
            pci_vendor_id=self._current_profile.pci_vendor_id,
            video_processor=self._name_edit.text() or self._current_profile.name,
            dac_type=self._current_profile.dac_type,
            features=self._current_profile.features,
            display_modes=self._current_profile.display_modes,
            registry_entries=self._current_profile.registry_entries
        )

    def _save_profile(self) -> None:
        """Save changes to current profile."""
        updated = self._get_profile_from_form()
        if not updated:
            return

        try:
            self._config_manager.save_profile(updated, overwrite=True)
            self._current_profile = updated
            self.profile_updated.emit(updated)

            QMessageBox.information(
                self, "Saved",
                f"Profile '{updated.name}' saved successfully!\n\n"
                f"VRAM: {updated.vram_mb // 1024} GB"
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save: {e}")

    def _save_as_new(self) -> None:
        """Save as a new profile."""
        updated = self._get_profile_from_form()
        if not updated:
            return

        # Create new ID
        base_name = updated.name.lower().replace(" ", "_")
        new_id = f"custom_{base_name}"

        new_profile = GPUProfile(
            id=new_id,
            name=f"{updated.name} (Custom)",
            manufacturer=updated.manufacturer,
            driver_version=updated.driver_version,
            driver_date=updated.driver_date,
            vram_mb=updated.vram_mb,
            vram_type=updated.vram_type,
            memory_bus_width=updated.memory_bus_width,
            base_clock_mhz=updated.base_clock_mhz,
            boost_clock_mhz=updated.boost_clock_mhz,
            memory_clock_mhz=updated.memory_clock_mhz,
            cuda_cores=updated.cuda_cores,
            stream_processors=updated.stream_processors,
            tdp_watts=updated.tdp_watts,
            pci_device_id=updated.pci_device_id,
            pci_vendor_id=updated.pci_vendor_id,
            video_processor=updated.video_processor,
            dac_type=updated.dac_type,
            features=updated.features,
            display_modes=updated.display_modes,
            registry_entries=updated.registry_entries
        )

        try:
            self._config_manager.save_profile(new_profile)
            self.profile_updated.emit(new_profile)

            QMessageBox.information(
                self, "Created",
                f"New profile '{new_profile.name}' created!\n\n"
                f"VRAM: {new_profile.vram_mb // 1024} GB"
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create: {e}")

    def _reset_form(self) -> None:
        """Reset form to original profile values."""
        if self._current_profile:
            self._update_form_from_profile(self._current_profile)

    def set_profile(self, profile: Optional[GPUProfile]) -> None:
        """Set the profile to edit."""
        self._current_profile = profile

        if profile:
            self._update_form_from_profile(profile)
        else:
            self._save_btn.setEnabled(False)
            self._save_as_btn.setEnabled(False)
