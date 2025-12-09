"""
Verification Panel
A panel showing verification steps with clickable launchers.
"""

import subprocess
import sys
import logging
from typing import Optional
from pathlib import Path

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QGroupBox, QGridLayout, QPushButton, QCheckBox, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

logger = logging.getLogger(__name__)


class VerificationStep(QFrame):
    """A single verification step with checkbox and action button."""

    def __init__(self, step_number: int, title: str, description: str,
                 button_text: str, command: str, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._command = command

        self.setFrameStyle(QFrame.Box | QFrame.Raised)
        self.setStyleSheet("""
            VerificationStep {
                background-color: #2d2d2d;
                border-radius: 5px;
                border: 1px solid #3d3d3d;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)

        # Checkbox (for user to mark completion)
        self._checkbox = QCheckBox()
        self._checkbox.setStyleSheet("""
            QCheckBox::indicator { width: 20px; height: 20px; }
            QCheckBox::indicator:checked { background-color: #76b900; }
        """)
        layout.addWidget(self._checkbox)

        # Step info
        info_layout = QVBoxLayout()

        step_label = QLabel(f"Step {step_number}: {title}")
        step_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        step_label.setStyleSheet("color: #ffffff;")
        info_layout.addWidget(step_label)

        desc_label = QLabel(description)
        desc_label.setStyleSheet("color: #888888; font-size: 10px;")
        desc_label.setWordWrap(True)
        info_layout.addWidget(desc_label)

        layout.addLayout(info_layout, 1)

        # Action button
        self._action_btn = QPushButton(button_text)
        self._action_btn.setStyleSheet("""
            QPushButton {
                background-color: #76b900;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #8bc34a;
            }
        """)
        self._action_btn.clicked.connect(self._on_action)
        layout.addWidget(self._action_btn)

    def _on_action(self):
        """Execute the verification action."""
        try:
            if self._command.startswith("ms-settings:"):
                # Open Windows Settings URI
                import os
                os.startfile(self._command)
            elif self._command == "nvidia_panel":
                # Launch NVIDIA Control Panel
                self._launch_nvidia_panel()
            elif self._command == "geforce_experience":
                # Launch GeForce Experience
                self._launch_geforce_experience()
            else:
                # Run as shell command
                subprocess.Popen(self._command, shell=True)

            # Auto-check the checkbox
            self._checkbox.setChecked(True)

        except Exception as e:
            QMessageBox.warning(
                self,
                "Error",
                f"Could not execute action:\n\n{str(e)}"
            )

    def _launch_nvidia_panel(self):
        """Launch the NVIDIA Control Panel."""
        # Try installed location first
        installed_path = Path(r"C:\Program Files\NVIDIA Corporation\Control Panel\NVIDIA Control Panel.bat")
        if installed_path.exists():
            subprocess.Popen(str(installed_path), shell=True)
        else:
            # Fall back to source location
            project_root = Path(__file__).parent.parent.parent
            run_script = project_root / "run_nvidia_panel.py"
            if run_script.exists():
                subprocess.Popen([sys.executable, str(run_script)])
            else:
                raise FileNotFoundError("NVIDIA Control Panel not found")

    def _launch_geforce_experience(self):
        """Launch GeForce Experience."""
        # Try installed location first
        installed_path = Path(r"C:\Program Files\NVIDIA Corporation\NVIDIA GeForce Experience\GeForce Experience.bat")
        if installed_path.exists():
            subprocess.Popen(str(installed_path), shell=True)
        else:
            # Fall back to source location
            project_root = Path(__file__).parent.parent.parent
            run_script = project_root / "run_geforce_experience.py"
            if run_script.exists():
                subprocess.Popen([sys.executable, str(run_script)])
            else:
                raise FileNotFoundError("GeForce Experience not found")


class VerificationPanel(QWidget):
    """Panel showing verification steps with clickable launchers."""

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._current_profile = None
        self._setup_ui()

    def set_profile(self, profile) -> None:
        """Set the current GPU profile (required by MainWindow)."""
        self._current_profile = profile
        # VerificationPanel doesn't need to display profile-specific info
        # but method must exist for MainWindow._on_profile_changed

    def _setup_ui(self) -> None:
        """Set up the panel UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header
        header = QLabel("Verification Checklist")
        header.setFont(QFont("Segoe UI", 20, QFont.Bold))
        header.setStyleSheet("color: #76b900;")
        layout.addWidget(header)

        subtitle = QLabel(
            "Follow these steps to verify your GPU simulation is working correctly.\n"
            "Click each button to open the corresponding tool, then check the box when verified."
        )
        subtitle.setStyleSheet("color: #888; font-size: 12px;")
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        layout.addSpacing(10)

        # Verification steps
        steps = [
            (1, "Restart Computer",
             "Registry changes require a restart to take full effect",
             "Reminder Only", ""),

            (2, "Check Task Manager",
             "Open Performance tab → GPU section to see your spoofed GPU",
             "Open Task Manager", "taskmgr"),

            (3, "Run DxDiag",
             "Check the Display tab to verify GPU name and VRAM",
             "Run DxDiag", "dxdiag"),

            (4, "Check Windows Settings",
             "System → Display → Advanced display → Display adapter properties",
             "Open Settings", "ms-settings:display"),

            (5, "Open NVIDIA Control Panel",
             "Verify System Information matches your selected GPU profile",
             "Open Control Panel", "nvidia_panel"),

            (6, "Open GeForce Experience (Optional)",
             "Verify GPU information in home screen",
             "Open GFE", "geforce_experience"),
        ]

        for step_num, title, desc, btn_text, cmd in steps:
            step_widget = VerificationStep(step_num, title, desc, btn_text, cmd)
            layout.addWidget(step_widget)

        layout.addStretch()

        # Footer with tips
        tips_group = QGroupBox("Tips")
        tips_layout = QVBoxLayout(tips_group)
        tips = [
            "• If Task Manager doesn't show GPU, ensure registry changes were applied as Administrator",
            "• Some detection tools (GPU-Z, HWiNFO) may still see real hardware",
            "• The NVIDIA icon should appear in the system tray after opening Control Panel",
        ]
        for tip in tips:
            tip_label = QLabel(tip)
            tip_label.setStyleSheet("color: #888; font-size: 11px;")
            tips_layout.addWidget(tip_label)

        layout.addWidget(tips_group)
