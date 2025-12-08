"""
GPU Info Panel
Displays detailed GPU profile information and allows editing.
"""

from typing import Optional
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox,
    QGridLayout, QTableWidget, QTableWidgetItem, QHeaderView,
    QPushButton, QTextEdit, QTabWidget, QScrollArea
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

import sys
sys.path.insert(0, str(__file__).rsplit('src', 1)[0])

from src.core.gpu_profile import GPUProfile


class GPUInfoPanel(QWidget):
    """
    Panel showing detailed GPU profile information.
    """

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._current_profile: Optional[GPUProfile] = None
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the panel UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header = QLabel("GPU Profile Details")
        header.setFont(QFont("Segoe UI", 18, QFont.Bold))
        layout.addWidget(header)

        # Tab widget for organization
        tabs = QTabWidget()

        # Specifications tab
        specs_tab = QWidget()
        specs_layout = QVBoxLayout(specs_tab)

        self._specs_table = QTableWidget()
        self._specs_table.setColumnCount(2)
        self._specs_table.setHorizontalHeaderLabels(["Property", "Value"])
        self._specs_table.horizontalHeader().setStretchLastSection(True)
        self._specs_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self._specs_table.setAlternatingRowColors(True)
        self._specs_table.setEditTriggers(QTableWidget.NoEditTriggers)
        specs_layout.addWidget(self._specs_table)

        tabs.addTab(specs_tab, "Specifications")

        # Registry Entries tab
        registry_tab = QWidget()
        registry_layout = QVBoxLayout(registry_tab)

        self._registry_text = QTextEdit()
        self._registry_text.setReadOnly(True)
        self._registry_text.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12px;
            }
        """)
        registry_layout.addWidget(self._registry_text)

        tabs.addTab(registry_tab, "Registry Entries")

        # Display Modes tab
        modes_tab = QWidget()
        modes_layout = QVBoxLayout(modes_tab)

        self._modes_table = QTableWidget()
        self._modes_table.setColumnCount(3)
        self._modes_table.setHorizontalHeaderLabels(["Width", "Height", "Refresh Rate"])
        self._modes_table.horizontalHeader().setStretchLastSection(True)
        self._modes_table.setAlternatingRowColors(True)
        self._modes_table.setEditTriggers(QTableWidget.NoEditTriggers)
        modes_layout.addWidget(self._modes_table)

        tabs.addTab(modes_tab, "Display Modes")

        layout.addWidget(tabs)

        # No profile message
        self._no_profile_label = QLabel("Select a GPU profile to view details")
        self._no_profile_label.setAlignment(Qt.AlignCenter)
        self._no_profile_label.setStyleSheet("color: #888; font-size: 14px;")
        layout.addWidget(self._no_profile_label)

        self._show_no_profile(True)

    def _show_no_profile(self, show: bool) -> None:
        """Toggle between profile view and no-profile message."""
        self._no_profile_label.setVisible(show)

    def set_profile(self, profile: Optional[GPUProfile]) -> None:
        """Update panel with a new profile."""
        self._current_profile = profile

        if not profile:
            self._show_no_profile(True)
            self._specs_table.setRowCount(0)
            self._registry_text.clear()
            self._modes_table.setRowCount(0)
            return

        self._show_no_profile(False)

        # Update specifications table
        specs = [
            ("Name", profile.name),
            ("ID", profile.id),
            ("Manufacturer", profile.manufacturer),
            ("", ""),
            ("VRAM", f"{profile.vram_mb} MB ({profile.vram_gb:.1f} GB)"),
            ("VRAM Type", profile.vram_type),
            ("Memory Bus Width", f"{profile.memory_bus_width} bit"),
            ("", ""),
            ("Base Clock", f"{profile.base_clock_mhz} MHz"),
            ("Boost Clock", f"{profile.boost_clock_mhz} MHz"),
            ("Memory Clock", f"{profile.memory_clock_mhz} MHz"),
            ("", ""),
            ("CUDA Cores", str(profile.cuda_cores) if profile.cuda_cores else "N/A"),
            ("Stream Processors", str(profile.stream_processors) if profile.stream_processors else "N/A"),
            ("TDP", f"{profile.tdp_watts} W"),
            ("", ""),
            ("Driver Version", profile.driver_version),
            ("Driver Date", profile.driver_date or "N/A"),
            ("PCI Device ID", profile.pci_device_id),
            ("PCI Vendor ID", profile.pci_vendor_id),
            ("", ""),
            ("Video Processor", profile.video_processor),
            ("DAC Type", profile.dac_type),
        ]

        # Add features
        if profile.features:
            specs.append(("", ""))
            specs.append(("--- Features ---", ""))
            for key, value in profile.features.items():
                specs.append((key, str(value)))

        self._specs_table.setRowCount(len(specs))
        for row, (prop, value) in enumerate(specs):
            self._specs_table.setItem(row, 0, QTableWidgetItem(prop))
            self._specs_table.setItem(row, 1, QTableWidgetItem(str(value)))

        # Update registry entries
        registry_text = "Registry entries that will be applied:\n\n"
        for key, value in profile.registry_entries.items():
            if isinstance(value, int):
                registry_text += f'{key} = 0x{value:X} ({value})\n'
            else:
                registry_text += f'{key} = "{value}"\n'
        self._registry_text.setText(registry_text)

        # Update display modes
        self._modes_table.setRowCount(len(profile.display_modes))
        for row, mode in enumerate(profile.display_modes):
            self._modes_table.setItem(row, 0, QTableWidgetItem(str(mode.width)))
            self._modes_table.setItem(row, 1, QTableWidgetItem(str(mode.height)))
            self._modes_table.setItem(row, 2, QTableWidgetItem(f"{mode.refresh} Hz"))
