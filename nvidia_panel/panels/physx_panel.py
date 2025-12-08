"""
PhysX Configuration Panel
Shows PhysX processor settings similar to real NVIDIA Control Panel.
"""

from typing import Optional
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox,
    QComboBox, QPushButton, QFrame, QGridLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.gpu_profile import GPUProfile


class PhysXPanel(QWidget):
    """
    PhysX Configuration panel.
    Shows PhysX processor selection like real NVIDIA Control Panel.
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
        header = QLabel("Configure PhysX")
        header.setFont(QFont("Segoe UI", 16, QFont.Bold))
        layout.addWidget(header)

        desc = QLabel(
            "PhysX is a physics processing engine developed by NVIDIA. "
            "Select the processor to use for PhysX acceleration."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #888;")
        layout.addWidget(desc)

        layout.addSpacing(20)

        # PhysX processor selection
        processor_group = QGroupBox("Select a PhysX processor")
        proc_layout = QVBoxLayout(processor_group)

        self._processor_combo = QComboBox()
        self._processor_combo.setMinimumWidth(300)
        proc_layout.addWidget(self._processor_combo)

        # Info label
        self._info_label = QLabel("")
        self._info_label.setStyleSheet("color: #76B900; margin-top: 10px;")
        proc_layout.addWidget(self._info_label)

        layout.addWidget(processor_group)

        # PhysX Visual Indicator
        visual_group = QGroupBox("PhysX Visual Indicator")
        visual_layout = QVBoxLayout(visual_group)

        self._visual_combo = QComboBox()
        self._visual_combo.addItems([
            "On (Show PhysX Visual Indicator)",
            "Off"
        ])
        self._visual_combo.setCurrentIndex(1)
        visual_layout.addWidget(self._visual_combo)

        layout.addWidget(visual_group)

        # System Information
        info_group = QGroupBox("PhysX System Information")
        info_layout = QGridLayout(info_group)

        info_layout.addWidget(QLabel("PhysX Version:"), 0, 0)
        self._physx_version = QLabel("9.21.0513")
        self._physx_version.setStyleSheet("color: #76B900;")
        info_layout.addWidget(self._physx_version, 0, 1)

        info_layout.addWidget(QLabel("PhysX GPU:"), 1, 0)
        self._physx_gpu = QLabel("-")
        self._physx_gpu.setStyleSheet("color: #76B900;")
        info_layout.addWidget(self._physx_gpu, 1, 1)

        info_layout.addWidget(QLabel("PhysX Driver:"), 2, 0)
        self._physx_driver = QLabel("-")
        self._physx_driver.setStyleSheet("color: #76B900;")
        info_layout.addWidget(self._physx_driver, 2, 1)

        layout.addWidget(info_group)

        # Apply button
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        apply_btn = QPushButton("Apply")
        apply_btn.setStyleSheet("background-color: #76B900; color: white; padding: 8px 20px;")
        btn_layout.addWidget(apply_btn)

        layout.addLayout(btn_layout)
        layout.addStretch()

    def set_profile(self, profile: Optional[GPUProfile]) -> None:
        """Set the GPU profile."""
        self._profile = profile

        if not profile:
            return

        # Update processor dropdown
        self._processor_combo.clear()
        self._processor_combo.addItems([
            "Auto-select (Recommended)",
            f"{profile.name} (dedicated)",
            "CPU"
        ])
        self._processor_combo.setCurrentIndex(0)

        # Update info
        if profile.features.get("cuda", False):
            self._info_label.setText(f"✓ PhysX acceleration available on {profile.name}")
        else:
            self._info_label.setText("⚠ PhysX acceleration requires NVIDIA GPU with CUDA")

        # Update system info
        self._physx_gpu.setText(profile.name)
        self._physx_driver.setText(profile.driver_version)
