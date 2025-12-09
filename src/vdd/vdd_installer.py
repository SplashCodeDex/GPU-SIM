"""
GPU-SIM Virtual Display Driver Installer
Handles installation and configuration of the MttVDD for Task Manager GPU spoofing.
Updated to use VirtualDrivers/Virtual-Display-Driver (MttVDD).
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
    """Virtual Display Driver installer for GPU-SIM using MttVDD."""

    # Install directory for MttVDD driver
    INSTALL_DIR = Path("C:/VirtualDisplayDriver")

    # Driver filenames for MttVDD
    DRIVER_DLL = "MttVDD.dll"
    DRIVER_INF = "MttVDD.inf"
    DRIVER_CAT = "mttvdd.cat"
    SETTINGS_XML = "vdd_settings.xml"

    def __init__(self, gpu_name: str = "NVIDIA GeForce GTX 780 Ti",
                 manufacturer: str = "NVIDIA Corporation"):
        self.gpu_name = gpu_name
        self.manufacturer = manufacturer

        # Path to built driver (relative to GPU-SIM root)
        self.driver_source = Path(__file__).parent.parent.parent / \
            "drivers/vdd/Virtual-Display-Driver/Virtual Display Driver (HDR)/x64/Release/MttVDD"

    def is_installed(self) -> bool:
        """Check if VDD is installed."""
        return (self.INSTALL_DIR / self.DRIVER_DLL).exists()

    def get_driver_source_path(self) -> Path:
        """Get path to built driver files."""
        # Check multiple possible locations
        possible_paths = [
            self.driver_source,
            Path(__file__).parent.parent.parent / "drivers/vdd/Virtual-Display-Driver/Virtual Display Driver (HDR)/x64/Release/MttVDD",
            Path("W:/CodeDeX/GPU-SIM/drivers/vdd/Virtual-Display-Driver/Virtual Display Driver (HDR)/x64/Release/MttVDD"),
        ]

        for path in possible_paths:
            if path.exists() and (path / self.DRIVER_DLL).exists():
                return path

        return self.driver_source

    def create_config_files(self) -> bool:
        """Create configuration files in install directory."""
        try:
            self.INSTALL_DIR.mkdir(parents=True, exist_ok=True)

            # Create default option.txt for virtual displays
            if not (self.INSTALL_DIR / "option.txt").exists():
                option_content = """1
# GPU-SIM Virtual Display Configuration
# Number of virtual displays (first line)
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

    def copy_driver_files(self, source_dir: Optional[Path] = None) -> bool:
        """Copy driver files to install directory."""
        if source_dir is None:
            source_dir = self.get_driver_source_path()

        required_files = [
            self.DRIVER_DLL,
            self.DRIVER_INF,
            self.DRIVER_CAT,
        ]

        optional_files = [
            self.SETTINGS_XML,
        ]

        try:
            self.INSTALL_DIR.mkdir(parents=True, exist_ok=True)

            copied = 0
            for filename in required_files:
                src = source_dir / filename
                if src.exists():
                    shutil.copy2(src, self.INSTALL_DIR / filename)
                    copied += 1
                else:
                    print(f"Warning: Required file not found: {src}")

            for filename in optional_files:
                src = source_dir / filename
                if src.exists():
                    shutil.copy2(src, self.INSTALL_DIR / filename)

            # Also copy vdd_settings.xml from parent directory if not in MttVDD folder
            settings_parent = source_dir.parent.parent / self.SETTINGS_XML
            if settings_parent.exists() and not (self.INSTALL_DIR / self.SETTINGS_XML).exists():
                shutil.copy2(settings_parent, self.INSTALL_DIR / self.SETTINGS_XML)

            return copied == len(required_files)
        except Exception as e:
            print(f"Error copying driver files: {e}")
            return False

    def install_driver(self) -> bool:
        """Install the VDD driver using pnputil."""
        if not is_admin():
            print("Administrator privileges required!")
            return False

        inf_path = self.INSTALL_DIR / self.DRIVER_INF
        if not inf_path.exists():
            print(f"Driver INF file not found at: {inf_path}")
            return False

        try:
            # Use pnputil to install the driver
            result = subprocess.run(
                ['pnputil', '/add-driver', str(inf_path), '/install'],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print("MttVDD driver installed successfully!")
                print("The virtual display should now appear in Device Manager.")
                return True
            else:
                print(f"Driver installation failed: {result.stderr}")
                print("You may need to install manually via Device Manager:")
                print("  1. Open Device Manager")
                print("  2. Action → Add Legacy Hardware")
                print("  3. Select 'Display adapters'")
                print("  4. Click 'Have Disk...' and browse to the INF file")
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
            # List drivers and find MttVDD
            result = subprocess.run(
                ['pnputil', '/enum-drivers'],
                capture_output=True,
                text=True
            )

            # Look for MttVDD and uninstall
            lines = result.stdout.split('\n')
            oem_inf = None
            for i, line in enumerate(lines):
                if 'MttVDD' in line or 'Virtual Display' in line:
                    # Find the OEM INF name from previous lines
                    for j in range(max(0, i-5), i):
                        if 'oem' in lines[j].lower() and '.inf' in lines[j].lower():
                            parts = lines[j].split(':')
                            if len(parts) > 1:
                                oem_inf = parts[1].strip()
                                break
                    break

            if oem_inf:
                result = subprocess.run(
                    ['pnputil', '/delete-driver', oem_inf, '/uninstall', '/force'],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    print("Driver uninstalled successfully!")
                    return True

            print("Driver not found or already uninstalled.")
            return False
        except Exception as e:
            print(f"Error uninstalling driver: {e}")
            return False

    def get_status(self) -> dict:
        """Get current VDD installation status."""
        return {
            "installed": self.is_installed(),
            "test_signing": is_test_signing_enabled(),
            "install_dir": str(self.INSTALL_DIR),
            "driver_source": str(self.get_driver_source_path()),
            "gpu_name": self.gpu_name,
            "manufacturer": self.manufacturer,
        }


def get_vdd_installer(gpu_name: str = "NVIDIA GeForce GTX 780 Ti") -> VDDInstaller:
    """Factory function to get VDD installer instance."""
    return VDDInstaller(gpu_name=gpu_name)


if __name__ == "__main__":
    print("GPU-SIM Virtual Display Driver Installer (MttVDD)")
    print("=" * 55)

    if not is_admin():
        print("WARNING: This script requires Administrator privileges for installation!")
        print("         Some operations may fail without admin rights.\n")

    installer = get_vdd_installer()
    status = installer.get_status()

    print(f"Test Signing Enabled: {status['test_signing']}")
    print(f"VDD Installed: {status['installed']}")
    print(f"Install Directory: {status['install_dir']}")
    print(f"Driver Source: {status['driver_source']}")
    print(f"GPU Name: {status['gpu_name']}")
    print()

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "install":
            if not is_admin():
                print("ERROR: Installation requires Administrator privileges!")
                sys.exit(1)

            if not is_test_signing_enabled():
                print("WARNING: Test signing is not enabled.")
                print("Run 'bcdedit /set testsigning on' and reboot first.")
                response = input("Continue anyway? (y/n): ")
                if response.lower() != 'y':
                    sys.exit(1)

            print("\nCopying driver files...")
            if installer.copy_driver_files():
                print("Driver files copied successfully!")
            else:
                print("Failed to copy driver files!")
                sys.exit(1)

            print("\nCreating config files...")
            if installer.create_config_files():
                print("Config files created successfully!")

            print("\nInstalling driver...")
            if installer.install_driver():
                print("\n✅ VDD installation complete!")
            else:
                sys.exit(1)

        elif command == "uninstall":
            if not is_admin():
                print("ERROR: Uninstallation requires Administrator privileges!")
                sys.exit(1)

            installer.uninstall_driver()

        elif command == "status":
            # Already printed above
            pass

        else:
            print(f"Unknown command: {command}")
            print("Usage: python vdd_installer.py [install|uninstall|status]")
    else:
        print("Usage: python vdd_installer.py [install|uninstall|status]")
        print("\nRun with 'install' to install the VDD driver.")
