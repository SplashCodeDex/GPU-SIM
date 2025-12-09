"""
GPU Registry Manager
Handles reading and modifying Windows registry entries for GPU simulation.
"""

import logging
import winreg
from typing import Dict, Optional, Any, List, Tuple
from pathlib import Path

from ..core.gpu_profile import GPUProfile
from .backup_manager import get_backup_manager

logger = logging.getLogger(__name__)


class GPURegistry:
    """
    Manages GPU-related Windows registry entries.
    Provides read/write access to display adapter registry keys.
    """

    # Registry base paths
    VIDEO_PATH = r"SYSTEM\CurrentControlSet\Control\Video"
    DISPLAY_CLASS_PATH = r"SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}"
    GRAPHICS_DRIVERS_PATH = r"SYSTEM\CurrentControlSet\Control\GraphicsDrivers"

    # Display adapter class GUID
    DISPLAY_CLASS_GUID = "{4d36e968-e325-11ce-bfc1-08002be10318}"

    def __init__(self, create_backups: bool = True):
        """
        Initialize the GPU registry manager.

        Args:
            create_backups: Whether to create backups before modifications.
        """
        self._create_backups = create_backups
        self._backup_manager = get_backup_manager() if create_backups else None
        logger.info("GPURegistry initialized")

    def _open_key(self, path: str, access: int = winreg.KEY_READ) -> Optional[winreg.HKEYType]:
        """
        Open a registry key.

        Args:
            path: Path relative to HKEY_LOCAL_MACHINE
            access: Access flags (KEY_READ, KEY_WRITE, etc.)

        Returns:
            Registry key handle, or None if failed.
        """
        try:
            return winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path, 0, access)
        except OSError as e:
            logger.debug(f"Could not open registry key {path}: {e}")
            return None

    def _get_subkeys(self, key: winreg.HKEYType) -> List[str]:
        """Get all subkey names under a registry key."""
        subkeys = []
        i = 0
        while True:
            try:
                subkeys.append(winreg.EnumKey(key, i))
                i += 1
            except OSError:
                break
        return subkeys

    def _get_values(self, key: winreg.HKEYType) -> Dict[str, Tuple[Any, int]]:
        """Get all values under a registry key."""
        values = {}
        i = 0
        while True:
            try:
                name, data, value_type = winreg.EnumValue(key, i)
                values[name] = (data, value_type)
                i += 1
            except OSError:
                break
        return values

    def get_display_adapters(self) -> List[Dict[str, Any]]:
        """
        Get information about all display adapters from registry.

        Returns:
            List of dictionaries containing adapter information.
        """
        adapters = []

        key = self._open_key(self.DISPLAY_CLASS_PATH)
        if not key:
            logger.warning("Could not open display class registry key")
            return adapters

        try:
            subkeys = self._get_subkeys(key)

            for subkey_name in subkeys:
                # Skip non-numeric subkeys
                if not subkey_name.isdigit():
                    continue

                adapter_path = f"{self.DISPLAY_CLASS_PATH}\\{subkey_name}"
                adapter_key = self._open_key(adapter_path)

                if adapter_key:
                    try:
                        values = self._get_values(adapter_key)
                        adapter_info = {
                            "index": subkey_name,
                            "path": adapter_path,
                        }

                        # Extract common values
                        for name, (data, _) in values.items():
                            if isinstance(data, bytes):
                                try:
                                    data = data.decode('utf-16-le').rstrip('\x00')
                                except UnicodeDecodeError:
                                    pass
                            adapter_info[name] = data

                        adapters.append(adapter_info)
                    finally:
                        winreg.CloseKey(adapter_key)
        finally:
            winreg.CloseKey(key)

        logger.info(f"Found {len(adapters)} display adapters in registry")
        return adapters

    def get_current_gpu_info(self) -> Optional[Dict[str, Any]]:
        """
        Get information about the primary GPU from registry.

        Returns:
            Dictionary with GPU information, or None if not found.
        """
        adapters = self.get_display_adapters()
        if not adapters:
            return None

        # Return the first adapter (typically the primary GPU)
        primary = adapters[0]

        return {
            "name": primary.get("DriverDesc", "Unknown GPU"),
            "manufacturer": primary.get("ProviderName", "Unknown"),
            "driver_version": primary.get("DriverVersion", "Unknown"),
            "driver_date": primary.get("DriverDate", ""),
            "device_id": primary.get("MatchingDeviceId", ""),
            "hardware_id": primary.get("HardwareID", ""),
        }

    def read_video_controller_info(self) -> List[Dict[str, Any]]:
        """
        Read video controller information from Control\\Video registry.

        Returns:
            List of video controller info dictionaries.
        """
        controllers = []

        key = self._open_key(self.VIDEO_PATH)
        if not key:
            return controllers

        try:
            # Each GUID subkey represents a video controller
            guids = self._get_subkeys(key)

            for guid in guids:
                if not guid.startswith("{"):
                    continue

                # Each controller has numbered subkeys (0000, 0001, etc.)
                controller_path = f"{self.VIDEO_PATH}\\{guid}\\0000"
                controller_key = self._open_key(controller_path)

                if controller_key:
                    try:
                        values = self._get_values(controller_key)
                        info = {"guid": guid, "path": controller_path}

                        for name, (data, _) in values.items():
                            if isinstance(data, bytes):
                                try:
                                    data = data.decode('utf-16-le').rstrip('\x00')
                                except UnicodeDecodeError:
                                    pass
                            info[name] = data

                        controllers.append(info)
                    finally:
                        winreg.CloseKey(controller_key)
        finally:
            winreg.CloseKey(key)

        return controllers

    def apply_gpu_profile(self, profile: GPUProfile, adapter_index: str = "0000") -> bool:
        """
        Apply a GPU profile's registry entries.

        ⚠️ WARNING: This modifies system registry. Use with caution!

        Args:
            profile: The GPUProfile to apply.
            adapter_index: The adapter index to modify (e.g., "0000").

        Returns:
            True if successful, False otherwise.
        """
        if self._create_backups and self._backup_manager:
            logger.info("Creating backup before applying GPU profile...")
            self._backup_manager.create_full_gpu_backup()

        adapter_path = f"{self.DISPLAY_CLASS_PATH}\\{adapter_index}"

        try:
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                adapter_path,
                0,
                winreg.KEY_WRITE | winreg.KEY_READ
            )
        except OSError as e:
            logger.error(f"Could not open adapter key for writing: {e}")
            logger.info("Make sure to run as Administrator!")
            return False

        try:
            # Apply registry entries from profile
            for name, value in profile.registry_entries.items():
                try:
                    if isinstance(value, int):
                        # qwMemorySize needs to be QWORD (64-bit) - write as binary
                        if 'qwMemorySize' in name:
                            # Convert to 8-byte little-endian binary for QWORD
                            binary_value = value.to_bytes(8, byteorder='little')
                            winreg.SetValueEx(key, name, 0, winreg.REG_BINARY, binary_value)
                        elif value > 0xFFFFFFFF:
                            # Value too large for DWORD, use QWORD
                            winreg.SetValueEx(key, name, 0, winreg.REG_QWORD, value)
                        else:
                            winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, value)
                    elif isinstance(value, str):
                        # Check if it's a multi-string or binary
                        if name.startswith("HardwareInformation."):
                            # Hardware info typically stored as REG_SZ
                            winreg.SetValueEx(key, name, 0, winreg.REG_SZ, value)
                        else:
                            winreg.SetValueEx(key, name, 0, winreg.REG_SZ, value)
                    elif isinstance(value, bytes):
                        winreg.SetValueEx(key, name, 0, winreg.REG_BINARY, value)

                    logger.debug(f"Set registry value: {name} = {value}")

                except OSError as e:
                    logger.error(f"Failed to set {name}: {e}")

            logger.info(f"Applied GPU profile: {profile.name}")
            return True

        except Exception as e:
            logger.error(f"Error applying GPU profile: {e}")
            return False
        finally:
            winreg.CloseKey(key)

    def get_graphics_drivers_config(self) -> Dict[str, Any]:
        """
        Get GraphicsDrivers configuration from registry.

        Returns:
            Dictionary of GraphicsDrivers settings.
        """
        config = {}
        key = self._open_key(self.GRAPHICS_DRIVERS_PATH)

        if key:
            try:
                values = self._get_values(key)
                for name, (data, _) in values.items():
                    config[name] = data
            finally:
                winreg.CloseKey(key)

        return config


# Singleton instance
_gpu_registry: Optional[GPURegistry] = None


def get_gpu_registry() -> GPURegistry:
    """Get the global GPURegistry instance."""
    global _gpu_registry
    if _gpu_registry is None:
        _gpu_registry = GPURegistry()
    return _gpu_registry
