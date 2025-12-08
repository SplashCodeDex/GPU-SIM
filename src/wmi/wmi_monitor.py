"""
WMI Monitor
Monitors and queries Windows Management Instrumentation for GPU information.
Shows what Windows and applications see regarding GPU hardware.
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# Try to import WMI module
try:
    import wmi
    WMI_AVAILABLE = True
except ImportError:
    WMI_AVAILABLE = False
    logger.warning("WMI module not available. Install with: pip install WMI")


@dataclass
class WMIVideoController:
    """Represents a video controller from WMI."""
    name: str
    adapter_ram: int
    adapter_ram_mb: float
    driver_version: str
    driver_date: str
    video_processor: str
    video_mode_description: str
    status: str
    pnp_device_id: str
    device_id: str
    adapter_compatibility: str
    dac_type: str

    @classmethod
    def from_wmi(cls, controller) -> "WMIVideoController":
        """Create instance from WMI Win32_VideoController object."""
        adapter_ram = controller.AdapterRAM or 0

        return cls(
            name=controller.Name or "Unknown",
            adapter_ram=adapter_ram,
            adapter_ram_mb=adapter_ram / (1024 * 1024) if adapter_ram else 0,
            driver_version=controller.DriverVersion or "Unknown",
            driver_date=controller.DriverDate or "",
            video_processor=controller.VideoProcessor or "",
            video_mode_description=controller.VideoModeDescription or "",
            status=controller.Status or "Unknown",
            pnp_device_id=controller.PNPDeviceID or "",
            device_id=controller.DeviceID or "",
            adapter_compatibility=controller.AdapterCompatibility or "",
            dac_type=controller.AdapterDACType or "",
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "adapter_ram_bytes": self.adapter_ram,
            "adapter_ram_mb": self.adapter_ram_mb,
            "driver_version": self.driver_version,
            "driver_date": self.driver_date,
            "video_processor": self.video_processor,
            "video_mode_description": self.video_mode_description,
            "status": self.status,
            "pnp_device_id": self.pnp_device_id,
            "device_id": self.device_id,
            "adapter_compatibility": self.adapter_compatibility,
            "dac_type": self.dac_type,
        }


class WMIMonitor:
    """
    Monitors WMI for GPU information.
    Provides insight into what Windows reports about GPUs.
    """

    def __init__(self):
        """Initialize the WMI monitor."""
        self._wmi = None
        self._connected = False
        self._connect()

    def _connect(self) -> bool:
        """Connect to WMI service."""
        if not WMI_AVAILABLE:
            logger.error("WMI module not available")
            return False

        try:
            self._wmi = wmi.WMI()
            self._connected = True
            logger.info("Connected to WMI service")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to WMI: {e}")
            return False

    @property
    def is_connected(self) -> bool:
        """Check if connected to WMI."""
        return self._connected

    def get_video_controllers(self) -> List[WMIVideoController]:
        """
        Get all video controllers from WMI.

        This is what Task Manager and other applications query.

        Returns:
            List of WMIVideoController objects.
        """
        if not self._connected:
            logger.warning("Not connected to WMI")
            return []

        try:
            controllers = []
            for controller in self._wmi.Win32_VideoController():
                controllers.append(WMIVideoController.from_wmi(controller))

            logger.info(f"Found {len(controllers)} video controllers via WMI")
            return controllers

        except Exception as e:
            logger.error(f"Error querying video controllers: {e}")
            return []

    def get_primary_gpu(self) -> Optional[WMIVideoController]:
        """
        Get the primary GPU from WMI.

        Returns:
            Primary WMIVideoController, or None if not found.
        """
        controllers = self.get_video_controllers()
        return controllers[0] if controllers else None

    def get_gpu_names(self) -> List[str]:
        """Get names of all GPUs."""
        return [c.name for c in self.get_video_controllers()]

    def get_total_vram_mb(self) -> float:
        """Get total VRAM across all GPUs in MB."""
        return sum(c.adapter_ram_mb for c in self.get_video_controllers())

    def query_display_configuration(self) -> List[Dict[str, Any]]:
        """
        Query display configuration from WMI.

        Returns:
            List of display configuration dictionaries.
        """
        if not self._connected:
            return []

        try:
            configs = []
            for config in self._wmi.Win32_DisplayConfiguration():
                configs.append({
                    "device_name": config.DeviceName,
                    "bits_per_pixel": config.BitsPerPixel,
                    "pels_width": config.PelsWidth,
                    "pels_height": config.PelsHeight,
                    "display_frequency": config.DisplayFrequency,
                    "driver_version": config.DriverVersion,
                })
            return configs
        except Exception as e:
            logger.error(f"Error querying display configuration: {e}")
            return []

    def query_desktop_monitor(self) -> List[Dict[str, Any]]:
        """
        Query desktop monitors from WMI.

        Returns:
            List of monitor information dictionaries.
        """
        if not self._connected:
            return []

        try:
            monitors = []
            for monitor in self._wmi.Win32_DesktopMonitor():
                monitors.append({
                    "name": monitor.Name,
                    "monitor_manufacturer": monitor.MonitorManufacturer,
                    "monitor_type": monitor.MonitorType,
                    "screen_width": monitor.ScreenWidth,
                    "screen_height": monitor.ScreenHeight,
                    "pnp_device_id": monitor.PNPDeviceID,
                })
            return monitors
        except Exception as e:
            logger.error(f"Error querying desktop monitors: {e}")
            return []

    def print_gpu_summary(self) -> None:
        """Print a summary of GPU information to console."""
        print("\n" + "=" * 60)
        print("GPU INFORMATION (as seen by Windows/WMI)")
        print("=" * 60)

        controllers = self.get_video_controllers()

        if not controllers:
            print("No video controllers found!")
            return

        for i, controller in enumerate(controllers, 1):
            print(f"\n[GPU {i}] {controller.name}")
            print("-" * 40)
            print(f"  VRAM: {controller.adapter_ram_mb:.0f} MB")
            print(f"  Driver Version: {controller.driver_version}")
            print(f"  Video Processor: {controller.video_processor}")
            print(f"  Current Mode: {controller.video_mode_description}")
            print(f"  DAC Type: {controller.dac_type}")
            print(f"  Status: {controller.status}")
            print(f"  PNP Device ID: {controller.pnp_device_id}")

        print("\n" + "=" * 60)


# Singleton instance
_wmi_monitor: Optional[WMIMonitor] = None


def get_wmi_monitor() -> WMIMonitor:
    """Get the global WMIMonitor instance."""
    global _wmi_monitor
    if _wmi_monitor is None:
        _wmi_monitor = WMIMonitor()
    return _wmi_monitor


# CLI entry point for standalone usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    monitor = get_wmi_monitor()
    monitor.print_gpu_summary()

    print("\n[Display Configuration]")
    for config in monitor.query_display_configuration():
        print(f"  {config}")

    print("\n[Desktop Monitors]")
    for mon in monitor.query_desktop_monitor():
        print(f"  {mon.get('name', 'Unknown')} - {mon.get('screen_width')}x{mon.get('screen_height')}")
