"""
VDD Panel
Panel for managing Virtual Display Driver installation.
"""

from typing import Optional
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox,
    QPushButton, QTextEdit, QProgressBar, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal

import sys
sys.path.insert(0, str(__file__).rsplit('src', 1)[0])

from src.core.gpu_profile import GPUProfile
from src.drivers.vdd_manager import get_vdd_manager, VDDInfo


class VDDPanel(QWidget):
    """
    Panel for Virtual Display Driver management.
    Shows installation status and provides download/install options.
    """

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._current_profile: Optional[GPUProfile] = None
        self._vdd_manager = get_vdd_manager()
        self._setup_ui()
        self._check_vdd_status()

    def _setup_ui(self) -> None:
        """Set up the panel UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header
        header = QLabel("Virtual Display Driver")
        header.setFont(QFont("Segoe UI", 18, QFont.Bold))
        layout.addWidget(header)

        subtitle = QLabel("Install a Virtual Display Driver to make the GPU appear in Windows")
        subtitle.setStyleSheet("color: #888;")
        layout.addWidget(subtitle)

        # Status section
        status_group = QGroupBox("Driver Status")
        status_layout = QVBoxLayout(status_group)

        self._status_label = QLabel("Checking...")
        self._status_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        status_layout.addWidget(self._status_label)

        self._status_detail = QLabel("")
        self._status_detail.setStyleSheet("color: #888;")
        status_layout.addWidget(self._status_detail)

        btn_layout = QHBoxLayout()
        self._refresh_btn = QPushButton("Refresh Status")
        self._refresh_btn.clicked.connect(self._check_vdd_status)
        btn_layout.addWidget(self._refresh_btn)
        btn_layout.addStretch()
        status_layout.addLayout(btn_layout)

        layout.addWidget(status_group)

        # Installation options
        install_group = QGroupBox("Installation Options")
        install_layout = QVBoxLayout(install_group)

        # Option 1: Virtual-Display-Driver
        opt1_layout = QHBoxLayout()
        opt1_info = QVBoxLayout()
        opt1_title = QLabel("Virtual-Display-Driver (Recommended)")
        opt1_title.setFont(QFont("Segoe UI", 11, QFont.Bold))
        opt1_info.addWidget(opt1_title)
        opt1_desc = QLabel("Open-source, signed driver. Easy installation.")
        opt1_desc.setStyleSheet("color: #888;")
        opt1_info.addWidget(opt1_desc)
        opt1_layout.addLayout(opt1_info)

        self._vdd_install_btn = QPushButton("Download")
        self._vdd_install_btn.clicked.connect(self._open_vdd_download)
        opt1_layout.addWidget(self._vdd_install_btn)

        install_layout.addLayout(opt1_layout)

        # Separator
        install_layout.addSpacing(10)

        # Option 2: Parsec VDD
        opt2_layout = QHBoxLayout()
        opt2_info = QVBoxLayout()
        opt2_title = QLabel("Parsec Virtual Display")
        opt2_title.setFont(QFont("Segoe UI", 11, QFont.Bold))
        opt2_info.addWidget(opt2_title)
        opt2_desc = QLabel("Supports up to 4K @ 240Hz. Requires Parsec account.")
        opt2_desc.setStyleSheet("color: #888;")
        opt2_info.addWidget(opt2_desc)
        opt2_layout.addLayout(opt2_info)

        self._parsec_install_btn = QPushButton("Download")
        self._parsec_install_btn.clicked.connect(self._open_parsec_download)
        opt2_layout.addWidget(self._parsec_install_btn)

        install_layout.addLayout(opt2_layout)

        layout.addWidget(install_group)

        # Instructions
        instructions_group = QGroupBox("Installation Instructions")
        instructions_layout = QVBoxLayout(instructions_group)

        instructions_text = QTextEdit()
        instructions_text.setReadOnly(True)
        instructions_text.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12px;
            }
        """)
        instructions_text.setText(self._vdd_manager.get_installation_instructions())
        instructions_text.setMaximumHeight(200)
        instructions_layout.addWidget(instructions_text)

        layout.addWidget(instructions_group)

        # What this does
        info_group = QGroupBox("How It Works")
        info_layout = QVBoxLayout(info_group)

        info_text = QLabel("""
<p>Virtual Display Drivers create a <b>real virtual monitor</b> in Windows that:</p>
<ul>
<li>Appears in Display Settings</li>
<li>Shows in Task Manager GPU tab</li>
<li>Visible in DxDiag</li>
<li>Works with remote desktop and streaming apps</li>
</ul>
<p>After installing a VDD, GPU-SIM can modify its registry entries to display
your chosen GPU specifications.</p>
        """)
        info_text.setWordWrap(True)
        info_text.setTextFormat(Qt.RichText)
        info_layout.addWidget(info_text)

        layout.addWidget(info_group)

        layout.addStretch()

    def _check_vdd_status(self) -> None:
        """Check if a VDD is installed."""
        vdd = self._vdd_manager.detect_installed_vdd()

        if vdd:
            self._status_label.setText(f"✅ {vdd.name}")
            self._status_label.setStyleSheet("color: #76b900;")
            self._status_detail.setText(f"Device ID: {vdd.device_id or 'Unknown'}")
        else:
            self._status_label.setText("❌ No Virtual Display Driver detected")
            self._status_label.setStyleSheet("color: #f44336;")
            self._status_detail.setText("Install a VDD for full GPU simulation")

    def _open_vdd_download(self) -> None:
        """Open Virtual-Display-Driver download page."""
        import webbrowser
        webbrowser.open("https://github.com/itsmikethetech/Virtual-Display-Driver/releases")

        QMessageBox.information(
            self,
            "Download Started",
            "The download page has been opened in your browser.\n\n"
            "After downloading:\n"
            "1. Run the installer as Administrator\n"
            "2. Restart your computer\n"
            "3. Click 'Refresh Status' to verify installation"
        )

    def _open_parsec_download(self) -> None:
        """Open Parsec VDD download page."""
        import webbrowser
        webbrowser.open("https://github.com/nomi-san/parsec-vdd/releases")

        QMessageBox.information(
            self,
            "Download Started",
            "The download page has been opened in your browser.\n\n"
            "Follow the installation instructions on the GitHub page."
        )

    def set_profile(self, profile: Optional[GPUProfile]) -> None:
        """Update panel with a GPU profile."""
        self._current_profile = profile
