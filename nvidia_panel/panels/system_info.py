"""
System Information Panel
Shows detailed GPU system information matching the spoofed profile.
"""

from typing import Optional
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox,
    QFormLayout, QFrame, QScrollArea, QTableWidget, QTableWidgetItem,
    QHeaderView
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.gpu_profile import GPUProfile


class SystemInfoPanel(QWidget):
    """
    System Information panel showing GPU details.
    Matches the real NVIDIA Control Panel "System Information" page.
    """

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._profile: Optional[GPUProfile] = None
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the panel UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header
        header = QLabel("System Information")
        header.setFont(QFont("Segoe UI", 16, QFont.Bold))
        layout.addWidget(header)

        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(20)

        # Graphics card information
        self._gpu_group = QGroupBox("Graphics card information:")
        gpu_layout = QFormLayout(self._gpu_group)
        gpu_layout.setSpacing(10)
        gpu_layout.setLabelAlignment(Qt.AlignLeft)

        self._name_label = QLabel("-")
        gpu_layout.addRow("Name:", self._name_label)

        self._manufacturer_label = QLabel("-")
        gpu_layout.addRow("Manufacturer:", self._manufacturer_label)

        self._gpu_type_label = QLabel("-")
        gpu_layout.addRow("GPU Type:", self._gpu_type_label)

        self._vram_label = QLabel("-")
        gpu_layout.addRow("Total available graphics memory:", self._vram_label)

        self._dedicated_label = QLabel("-")
        gpu_layout.addRow("Dedicated video memory:", self._dedicated_label)

        self._system_video_label = QLabel("-")
        gpu_layout.addRow("System video memory:", self._system_video_label)

        self._shared_label = QLabel("-")
        gpu_layout.addRow("Shared system memory:", self._shared_label)

        content_layout.addWidget(self._gpu_group)

        # Driver information
        self._driver_group = QGroupBox("Driver information:")
        driver_layout = QFormLayout(self._driver_group)
        driver_layout.setSpacing(10)

        self._driver_version_label = QLabel("-")
        driver_layout.addRow("Driver version:", self._driver_version_label)

        self._driver_date_label = QLabel("-")
        driver_layout.addRow("Driver date:", self._driver_date_label)

        self._directx_label = QLabel("-")
        driver_layout.addRow("Direct3D feature level:", self._directx_label)

        self._cuda_label = QLabel("-")
        driver_layout.addRow("CUDA Cores:", self._cuda_label)

        content_layout.addWidget(self._driver_group)

        # Features table
        self._features_group = QGroupBox("Component information:")
        features_layout = QVBoxLayout(self._features_group)

        self._features_table = QTableWidget()
        self._features_table.setColumnCount(2)
        self._features_table.setHorizontalHeaderLabels(["Component", "Status"])
        self._features_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._features_table.verticalHeader().setVisible(False)
        self._features_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self._features_table.setAlternatingRowColors(True)
        features_layout.addWidget(self._features_table)

        content_layout.addWidget(self._features_group)

        content_layout.addStretch()

        scroll.setWidget(content)
        layout.addWidget(scroll)

    def set_profile(self, profile: Optional[GPUProfile]) -> None:
        """Update the panel with a GPU profile."""
        self._profile = profile

        if not profile:
            return

        # Update GPU info
        self._name_label.setText(profile.name)
        self._manufacturer_label.setText(profile.manufacturer)
        self._gpu_type_label.setText(profile.video_processor or profile.name)
        self._vram_label.setText(f"{profile.vram_mb} MB")
        self._dedicated_label.setText(f"{profile.vram_mb} MB")
        self._system_video_label.setText("0 MB")
        self._shared_label.setText("16384 MB")  # Fake shared memory

        # Update driver info
        self._driver_version_label.setText(profile.driver_version)
        self._driver_date_label.setText(profile.driver_date)
        self._directx_label.setText(profile.features.get("directx", "12"))

        if profile.cuda_cores > 0:
            self._cuda_label.setText(f"{profile.cuda_cores}")
        elif profile.stream_processors > 0:
            self._cuda_label.setText(f"{profile.stream_processors} (Stream Processors)")
        else:
            self._cuda_label.setText("N/A")

        # Update features table
        self._update_features_table(profile)

    def _update_features_table(self, profile: GPUProfile) -> None:
        """Update the features table."""
        features = [
            ("NVIDIA nView", "Enabled" if profile.is_nvidia else "N/A"),
            ("PhysX", "Enabled" if profile.features.get("cuda", False) else "Disabled"),
            ("CUDA", "Enabled" if profile.features.get("cuda", False) else "Disabled"),
            ("OpenGL", profile.features.get("opengl", "4.6")),
            ("Vulkan", profile.features.get("vulkan", "1.3")),
            ("Ray Tracing", "Supported" if profile.features.get("ray_tracing", False) else "Not Supported"),
            ("DLSS", profile.features.get("dlss_version", "Supported") if profile.features.get("dlss", False) else "Not Supported"),
            ("NVENC", "Supported" if profile.features.get("nvenc", False) else "Not Supported"),
            ("AV1 Encode", "Supported" if profile.features.get("av1_encode", False) else "Not Supported"),
        ]

        self._features_table.setRowCount(len(features))
        for i, (component, status) in enumerate(features):
            self._features_table.setItem(i, 0, QTableWidgetItem(component))
            self._features_table.setItem(i, 1, QTableWidgetItem(status))
