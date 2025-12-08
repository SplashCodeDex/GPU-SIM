"""
Virtual Display Driver Manager
Handles downloading, installing, and managing Virtual Display Drivers.
"""

import os
import sys
import logging
import subprocess
import tempfile
import shutil
import urllib.request
import zipfile
from pathlib import Path
from typing import Optional, List, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class VDDInfo:
    """Information about an installed Virtual Display Driver."""
    name: str
    version: str
    installed: bool
    device_id: Optional[str] = None
    path: Optional[Path] = None


class VDDManager:
    """
    Manager for Virtual Display Drivers.
    Supports multiple VDD implementations.
    """

    # Known VDD projects
    VDD_SOURCES = {
        "virtual-display-driver": {
            "name": "Virtual Display Driver",
            "repo": "itsmikethetech/Virtual-Display-Driver",
            "releases_url": "https://github.com/itsmikethetech/Virtual-Display-Driver/releases",
            "device_class": "{4d36e968-e325-11ce-bfc1-08002be10318}",
        },
        "parsec-vdd": {
            "name": "Parsec Virtual Display",
            "repo": "nomi-san/parsec-vdd",
            "releases_url": "https://github.com/nomi-san/parsec-vdd/releases",
            "device_class": "{4d36e968-e325-11ce-bfc1-08002be10318}",
        }
    }

    def __init__(self, install_dir: Optional[Path] = None):
        """
        Initialize VDD Manager.

        Args:
            install_dir: Directory for VDD files. Defaults to project driver/ folder.
        """
        if install_dir:
            self._install_dir = Path(install_dir)
        else:
            # Default to project driver directory
            project_root = Path(__file__).parent.parent.parent
            self._install_dir = project_root / "driver" / "vdd"

        self._install_dir.mkdir(parents=True, exist_ok=True)
        self._installed_vdd: Optional[VDDInfo] = None

    @property
    def install_dir(self) -> Path:
        return self._install_dir

    def is_admin(self) -> bool:
        """Check if running with administrator privileges."""
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False

    def detect_installed_vdd(self) -> Optional[VDDInfo]:
        """
        Detect any installed Virtual Display Drivers.

        Returns:
            VDDInfo if a VDD is found, None otherwise.
        """
        try:
            import winreg

            # Check for Virtual Display Driver in device class
            class_path = r"SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}"

            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, class_path) as class_key:
                i = 0
                while True:
                    try:
                        subkey_name = winreg.EnumKey(class_key, i)
                        subkey_path = f"{class_path}\\{subkey_name}"

                        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, subkey_path) as subkey:
                            try:
                                driver_desc, _ = winreg.QueryValueEx(subkey, "DriverDesc")

                                # Check for known VDD signatures
                                vdd_signatures = [
                                    "Virtual Display",
                                    "IddSample",
                                    "Parsec",
                                    "GPU-SIM",
                                ]

                                for sig in vdd_signatures:
                                    if sig.lower() in str(driver_desc).lower():
                                        logger.info(f"Found VDD: {driver_desc}")
                                        self._installed_vdd = VDDInfo(
                                            name=driver_desc,
                                            version="Unknown",
                                            installed=True,
                                            device_id=subkey_name
                                        )
                                        return self._installed_vdd
                            except FileNotFoundError:
                                pass

                        i += 1
                    except OSError:
                        break

        except Exception as e:
            logger.error(f"Error detecting VDD: {e}")

        return None

    def get_devcon_path(self) -> Optional[Path]:
        """
        Get path to devcon.exe if available.
        DevCon is needed for driver installation.
        """
        # Check common locations
        search_paths = [
            Path(os.environ.get("ProgramFiles", "C:\\Program Files")) / "Windows Kits" / "10" / "Tools",
            Path(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")) / "Windows Kits" / "10" / "Tools",
            self._install_dir / "tools",
        ]

        for base_path in search_paths:
            if base_path.exists():
                # Search for devcon.exe
                for devcon in base_path.rglob("devcon.exe"):
                    logger.info(f"Found devcon at: {devcon}")
                    return devcon

        return None

    def create_virtual_device(self, hardware_id: str = "Root\\GPU_SIM") -> bool:
        """
        Create a virtual device node using devcon or pnputil.

        Args:
            hardware_id: Hardware ID for the virtual device.

        Returns:
            True if successful.
        """
        if not self.is_admin():
            logger.error("Administrator privileges required")
            return False

        # Try pnputil first (available on all Windows)
        try:
            result = subprocess.run(
                ["pnputil", "/enum-devices", "/class", "Display"],
                capture_output=True,
                text=True
            )
            logger.debug(f"PnPUtil output: {result.stdout}")
            return True
        except Exception as e:
            logger.error(f"PnPUtil error: {e}")

        return False

    def download_vdd(self, source: str = "virtual-display-driver") -> Optional[Path]:
        """
        Download a Virtual Display Driver package.

        Args:
            source: Which VDD to download (key from VDD_SOURCES).

        Returns:
            Path to downloaded file, or None on failure.
        """
        if source not in self.VDD_SOURCES:
            logger.error(f"Unknown VDD source: {source}")
            return None

        vdd_info = self.VDD_SOURCES[source]
        download_url = f"https://github.com/{vdd_info['repo']}/releases/latest/download/VirtualDisplayDriver.zip"

        logger.info(f"Downloading {vdd_info['name']} from {download_url}")

        try:
            # Download to temp file
            download_path = self._install_dir / "VirtualDisplayDriver.zip"
            urllib.request.urlretrieve(download_url, download_path)

            logger.info(f"Downloaded to: {download_path}")
            return download_path

        except Exception as e:
            logger.error(f"Download failed: {e}")
            return None

    def install_vdd_from_zip(self, zip_path: Path) -> bool:
        """
        Install VDD from a downloaded zip file.

        Args:
            zip_path: Path to the VDD zip file.

        Returns:
            True if installation was successful.
        """
        if not self.is_admin():
            logger.error("Administrator privileges required for installation")
            return False

        try:
            # Extract zip
            extract_dir = self._install_dir / "extracted"
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)

            logger.info(f"Extracted to: {extract_dir}")

            # Find INF file
            inf_files = list(extract_dir.rglob("*.inf"))
            if not inf_files:
                logger.error("No INF file found in package")
                return False

            inf_path = inf_files[0]
            logger.info(f"Found INF: {inf_path}")

            # Install using pnputil
            result = subprocess.run(
                ["pnputil", "/add-driver", str(inf_path), "/install"],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                logger.info("Driver installed successfully")
                return True
            else:
                logger.error(f"Installation failed: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"Installation error: {e}")
            return False

    def get_installation_instructions(self) -> str:
        """
        Get manual installation instructions.

        Returns:
            Formatted instruction string.
        """
        return """
╔═══════════════════════════════════════════════════════════════╗
║           Virtual Display Driver Installation Guide           ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║ Option 1: Virtual-Display-Driver (Recommended)                ║
║ ─────────────────────────────────────────────                 ║
║ 1. Download from:                                             ║
║    https://github.com/itsmikethetech/Virtual-Display-Driver   ║
║                                                               ║
║ 2. Run the installer as Administrator                         ║
║                                                               ║
║ 3. Restart your computer                                      ║
║                                                               ║
║ 4. GPU-SIM will detect the VDD and can modify it              ║
║                                                               ║
║ Option 2: Parsec VDD                                          ║
║ ────────────────────                                          ║
║ 1. Download from:                                             ║
║    https://github.com/nomi-san/parsec-vdd                     ║
║                                                               ║
║ 2. Follow their installation guide                            ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"""


# Singleton instance
_vdd_manager: Optional[VDDManager] = None

def get_vdd_manager() -> VDDManager:
    """Get the singleton VDD Manager instance."""
    global _vdd_manager
    if _vdd_manager is None:
        _vdd_manager = VDDManager()
    return _vdd_manager


if __name__ == "__main__":
    # CLI test
    logging.basicConfig(level=logging.INFO)

    manager = get_vdd_manager()

    print("\n" + "=" * 50)
    print("  VDD Manager - Virtual Display Driver Tool")
    print("=" * 50)

    print(f"\nInstall directory: {manager.install_dir}")
    print(f"Running as admin: {manager.is_admin()}")

    vdd = manager.detect_installed_vdd()
    if vdd:
        print(f"\n✅ Found VDD: {vdd.name}")
    else:
        print("\n❌ No Virtual Display Driver detected")
        print(manager.get_installation_instructions())
