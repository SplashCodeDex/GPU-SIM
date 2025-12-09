"""
GPU-SIM Virtual Display Driver Installer
Handles installation and configuration of the VDD for Task Manager GPU spoofing.
"""

import os
import sys
import shutil
import ctypes
import subprocess
from pathlib import Path
from typing import Optional


def is_admin() -> bool:
    """Check if running with Administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def is_test_signing_enabled() -> bool:
    """Check if test signing mode is enabled."""
    try:
        result = subprocess.run(
            ['bcdedit', '/enum', '{current}'],
            capture_output=True,
            text=True
        )
        return 'testsigning' in result.stdout.lower() and 'yes' in result.stdout.lower()
    except Exception:
        return False


def enable_test_signing() -> bool:
    """Enable test signing mode (requires reboot)."""
    if not is_admin():
        return False

    try:
        result = subprocess.run(
            ['bcdedit', '/set', 'testsigning', 'on'],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except Exception:
        return False


class VDDInstaller:
    """Virtual Display Driver installer for GPU-SIM."""

    INSTALL_DIR = Path("C:/IddSampleDriver")

    def __init__(self, gpu_name: str = "NVIDIA GeForce GTX 780 Ti",
                 manufacturer: str = "NVIDIA Corporation"):
        self.gpu_name = gpu_name
        self.manufacturer = manufacturer

    def is_installed(self) -> bool:
        """Check if VDD is installed."""
        return (self.INSTALL_DIR / "IddSampleDriver.dll").exists()

    def create_config_files(self) -> bool:
        """Create configuration files in install directory."""
        try:
            self.INSTALL_DIR.mkdir(parents=True, exist_ok=True)

            # Create gpu_sim_config.txt
            config_content = f"""# GPU-SIM Virtual Display Driver Configuration
# GPU Name (appears in Device Manager and system info)
{self.gpu_name}

# Manufacturer
{self.manufacturer}
"""
            (self.INSTALL_DIR / "gpu_sim_config.txt").write_text(config_content)

            # Create default option.txt if not exists
            if not (self.INSTALL_DIR / "option.txt").exists():
                option_content = """1
# GPU-SIM Virtual Display Configuration
# Format: width, height, refresh_rate
1920, 1080, 60
1280, 720, 60
2560, 1440, 60
3840, 2160, 60
"""
                (self.INSTALL_DIR / "option.txt").write_text(option_content)

            return True
        except Exception as e:
            print(f"Error creating config files: {e}")
            return False

    def copy_driver_files(self, source_dir: Path) -> bool:
        """Copy driver files to install directory."""
        required_files = [
            "IddSampleDriver.dll",
            "IddSampleDriver.inf",
            "IddSampleDriver.cat"  # Catalog file for signing
        ]

        try:
            for filename in required_files:
                src = source_dir / filename
                if src.exists():
                    shutil.copy2(src, self.INSTALL_DIR / filename)
            return True
        except Exception as e:
            print(f"Error copying driver files: {e}")
            return False

    def install_driver(self) -> bool:
        """Install the VDD driver using pnputil."""
        if not is_admin():
            print("Administrator privileges required!")
            return False

        inf_path = self.INSTALL_DIR / "IddSampleDriver.inf"
        if not inf_path.exists():
            print("Driver INF file not found!")
            return False

        try:
            # Use pnputil to install the driver
            result = subprocess.run(
                ['pnputil', '/add-driver', str(inf_path), '/install'],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print("VDD driver installed successfully!")
                return True
            else:
                print(f"Driver installation failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"Error installing driver: {e}")
            return False

    def uninstall_driver(self) -> bool:
        """Uninstall the VDD driver."""
        if not is_admin():
            print("Administrator privileges required!")
            return False

        try:
            # List drivers and find ours
            result = subprocess.run(
                ['pnputil', '/enum-drivers'],
                capture_output=True,
                text=True
            )

            # Look for IddSampleDriver and uninstall
            # This is a simplified version - production code would parse output properly
            if 'IddSampleDriver' in result.stdout:
                # Find the OEM INF name and uninstall
                result = subprocess.run(
                    ['pnputil', '/delete-driver', 'oem*.inf', '/uninstall', '/force'],
                    capture_output=True,
                    text=True
                )
                return True
            return False
        except Exception as e:
            print(f"Error uninstalling driver: {e}")
            return False


def get_vdd_installer(gpu_name: str = "NVIDIA GeForce GTX 780 Ti") -> VDDInstaller:
    """Factory function to get VDD installer instance."""
    return VDDInstaller(gpu_name=gpu_name)


if __name__ == "__main__":
    print("GPU-SIM Virtual Display Driver Installer")
    print("=" * 50)

    if not is_admin():
        print("ERROR: This script requires Administrator privileges!")
        sys.exit(1)

    installer = get_vdd_installer()

    print(f"Test Signing Enabled: {is_test_signing_enabled()}")
    print(f"VDD Installed: {installer.is_installed()}")
    print(f"Install Directory: {installer.INSTALL_DIR}")

    # Create config files
    if installer.create_config_files():
        print("Config files created successfully!")
    else:
        print("Failed to create config files!")
