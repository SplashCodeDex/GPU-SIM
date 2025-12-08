"""
GPU-Z / DirectX Detection Bypass
Provides hooks and spoofing for GPU detection tools.
"""

import logging
import ctypes
from ctypes import wintypes
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.gpu_profile import GPUProfile

logger = logging.getLogger(__name__)


@dataclass
class FakeAdapterInfo:
    """Fake DirectX adapter information."""
    description: str
    vendor_id: int
    device_id: int
    subsys_id: int
    revision: int
    dedicated_video_memory: int
    dedicated_system_memory: int
    shared_system_memory: int


class GPUZBypass:
    """
    Provides methods to make fake GPU visible to detection tools.

    GPU-Z reads from multiple sources:
    1. Registry (handled by registry module)
    2. WMI (handled by WMI module)
    3. DirectX DXGI EnumAdapters
    4. NVML/ADL SDKs (NVIDIA/AMD specific)
    5. Direct PCI access

    This module focuses on DirectX-level spoofing.
    """

    # DXGI constants
    DXGI_ADAPTER_FLAG_NONE = 0
    DXGI_ADAPTER_FLAG_REMOTE = 1
    DXGI_ADAPTER_FLAG_SOFTWARE = 2

    def __init__(self, profile: Optional[GPUProfile] = None):
        self._profile = profile
        self._fake_adapter: Optional[FakeAdapterInfo] = None
        self._hooks_installed = False

        if profile:
            self._create_fake_adapter(profile)

    def _create_fake_adapter(self, profile: GPUProfile) -> None:
        """Create fake adapter info from profile."""
        # Parse vendor/device IDs
        vendor_id = 0x10DE  # NVIDIA default
        device_id = 0x2684  # RTX 4090 default

        if profile.pci_vendor_id:
            try:
                vendor_id = int(profile.pci_vendor_id, 16)
            except ValueError:
                pass

        if profile.pci_device_id:
            try:
                # Format: VENDOR-DEVICE
                parts = profile.pci_device_id.split("-")
                if len(parts) == 2:
                    device_id = int(parts[1], 16)
                else:
                    device_id = int(profile.pci_device_id, 16)
            except ValueError:
                pass

        self._fake_adapter = FakeAdapterInfo(
            description=profile.name,
            vendor_id=vendor_id,
            device_id=device_id,
            subsys_id=0,
            revision=0xA1,
            dedicated_video_memory=profile.vram_mb * 1024 * 1024,
            dedicated_system_memory=0,
            shared_system_memory=0
        )

        logger.info(f"Created fake adapter: {profile.name}")

    def set_profile(self, profile: GPUProfile) -> None:
        """Update the spoofed GPU profile."""
        self._profile = profile
        self._create_fake_adapter(profile)

    def get_dxdiag_compatible_info(self) -> Dict[str, Any]:
        """
        Get GPU info in a format compatible with DxDiag.
        Can be used to generate fake DxDiag output.
        """
        if not self._fake_adapter:
            return {}

        return {
            "szDescription": self._fake_adapter.description,
            "szManufacturer": self._get_manufacturer_name(self._fake_adapter.vendor_id),
            "szChipType": self._profile.features.get("chip_type", "Unknown"),
            "szDACType": self._profile.dac_type if self._profile else "Integrated RAMDAC",
            "szDeviceType": "Full Device",
            "szDeviceKey": f"Enum\\PCI\\VEN_{self._fake_adapter.vendor_id:04X}&DEV_{self._fake_adapter.device_id:04X}",
            "szDisplayMemoryLocalized": f"{self._fake_adapter.dedicated_video_memory // (1024*1024)} MB",
            "szDisplayMemoryEnglish": f"{self._fake_adapter.dedicated_video_memory // (1024*1024)} MB",
            "szDriverName": "nvldumdx.dll,nvldumdx.dll",
            "szDriverVersion": self._profile.driver_version if self._profile else "1.0.0",
            "szDriverDateLocalized": self._profile.driver_date if self._profile else "1/1/2024",
            "szVendorId": f"0x{self._fake_adapter.vendor_id:04X}",
            "szDeviceId": f"0x{self._fake_adapter.device_id:04X}",
            "szSubSysId": f"0x{self._fake_adapter.subsys_id:08X}",
            "szRevisionId": f"0x{self._fake_adapter.revision:04X}",
            "b3DAPIsAvail": True,
            "bAGPEnabled": False,
            "bAGPExistenceValid": True,
            "bDDPoweredUp": True,
        }

    def _get_manufacturer_name(self, vendor_id: int) -> str:
        """Get manufacturer name from vendor ID."""
        vendors = {
            0x10DE: "NVIDIA",
            0x1002: "AMD",
            0x8086: "Intel",
            0x1414: "Microsoft",
        }
        return vendors.get(vendor_id, "Unknown")

    def generate_fake_gpuz_data(self) -> Dict[str, Any]:
        """
        Generate data that mimics GPU-Z output format.
        This can be used to create a fake GPU-Z sensor file.
        """
        if not self._profile or not self._fake_adapter:
            return {}

        return {
            "name": self._profile.name,
            "GPU": self._profile.video_processor,
            "vendor": self._get_manufacturer_name(self._fake_adapter.vendor_id),
            "subvendor": self._get_manufacturer_name(self._fake_adapter.vendor_id),
            "device_id": f"{self._fake_adapter.vendor_id:04X}-{self._fake_adapter.device_id:04X}",
            "revision": f"A{self._fake_adapter.revision & 0xF}",
            "process": "5nm" if "40" in self._profile.name else "8nm",
            "transistors": "76300M" if "4090" in self._profile.name else "28300M",
            "die_size": "608 mm²" if "4090" in self._profile.name else "392 mm²",
            "BIOS": self._profile.registry_entries.get("HardwareInformation.BiosString", "Unknown"),
            "driver_version": self._profile.driver_version,
            "driver_date": self._profile.driver_date,
            "digital_signature": "WHQL",

            # Memory
            "memory_type": self._profile.vram_type,
            "memory_size": f"{self._profile.vram_mb} MB",
            "memory_bus_width": f"{self._profile.memory_bus_width} bit",
            "memory_bandwidth": f"{self._profile.memory_clock_mhz * self._profile.memory_bus_width // 8 / 1000:.0f} GB/s",

            # Clocks
            "gpu_clock": f"{self._profile.base_clock_mhz} MHz",
            "boost_clock": f"{self._profile.boost_clock_mhz} MHz",
            "memory_clock": f"{self._profile.memory_clock_mhz} MHz",

            # Shaders
            "shaders": self._profile.cuda_cores or self._profile.stream_processors,
            "tmus": (self._profile.cuda_cores or self._profile.stream_processors) // 32,
            "rops": 128 if self._profile.vram_mb >= 16384 else 64,

            # Power
            "tdp": f"{self._profile.tdp_watts} W",
            "power_connectors": "16-pin" if self._profile.tdp_watts > 300 else "8-pin",

            # Features
            "directx": self._profile.features.get("directx", "12"),
            "opengl": self._profile.features.get("opengl", "4.6"),
            "vulkan": self._profile.features.get("vulkan", "1.3"),
            "opencl": "3.0",
            "cuda": self._profile.features.get("cuda", False),
            "ray_tracing": self._profile.features.get("ray_tracing", False),
        }

    def create_dxdiag_xml(self, output_path: Path) -> bool:
        """
        Create a fake DxDiag XML output file.
        Some applications parse saved DxDiag files.
        """
        if not self._profile:
            return False

        info = self.get_dxdiag_compatible_info()

        xml_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<DxDiag>
  <SystemInfo>
    <Time>12:00:00</Time>
    <MachineName>GPU-SIM</MachineName>
    <OperatingSystem>Windows 11 Pro 64-bit</OperatingSystem>
  </SystemInfo>
  <DisplayDevices>
    <DisplayDevice>
      <CardName>{info.get('szDescription', 'Unknown')}</CardName>
      <Manufacturer>{info.get('szManufacturer', 'Unknown')}</Manufacturer>
      <ChipType>{info.get('szChipType', 'Unknown')}</ChipType>
      <DACType>{info.get('szDACType', 'Integrated RAMDAC')}</DACType>
      <DeviceType>Full Device</DeviceType>
      <DisplayMemory>{info.get('szDisplayMemoryEnglish', '0 MB')}</DisplayMemory>
      <DedicatedMemory>{self._profile.vram_mb} MB</DedicatedMemory>
      <SharedMemory>0 MB</SharedMemory>
      <DriverVersion>{info.get('szDriverVersion', '1.0.0')}</DriverVersion>
      <DriverDate>{info.get('szDriverDateLocalized', '1/1/2024')}</DriverDate>
      <VendorID>{info.get('szVendorId', '0x0000')}</VendorID>
      <DeviceID>{info.get('szDeviceId', '0x0000')}</DeviceID>
      <FeatureLevels>12_1,12_0,11_1,11_0,10_1,10_0,9_3,9_2,9_1</FeatureLevels>
      <DirectXDriverVersion>12</DirectXDriverVersion>
    </DisplayDevice>
  </DisplayDevices>
</DxDiag>'''

        try:
            output_path.write_text(xml_content, encoding='utf-8')
            logger.info(f"Created fake DxDiag XML: {output_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to create DxDiag XML: {e}")
            return False

    def get_hook_instructions(self) -> str:
        """
        Get instructions for advanced API hooking.
        True GPU-Z bypass requires DLL injection or driver-level hooks.
        """
        return """
╔═══════════════════════════════════════════════════════════════╗
║              GPU-Z Detection Bypass - Advanced                ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║ GPU-Z reads from multiple sources:                            ║
║                                                               ║
║ ✅ Registry           - Covered by GPU-SIM registry module    ║
║ ✅ WMI                 - Covered by GPU-SIM WMI module         ║
║ ⚠️ DirectX DXGI       - Requires DLL hook (advanced)          ║
║ ⚠️ NVML/ADL           - Vendor SDK (not easily spoofable)     ║
║ ❌ Direct PCI         - Requires driver (not implemented)     ║
║                                                               ║
║ For complete GPU-Z bypass, you need:                          ║
║                                                               ║
║ 1. Install Virtual Display Driver (creates real adapter)      ║
║ 2. Apply GPU-SIM registry modifications                       ║
║ 3. (Optional) Use DLL hook for DXGI                           ║
║                                                               ║
║ The VDD approach is recommended as it creates a real          ║
║ virtual display adapter that Windows recognizes.              ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"""


# Singleton
_gpuz_bypass: Optional[GPUZBypass] = None

def get_gpuz_bypass() -> GPUZBypass:
    """Get the singleton GPU-Z bypass instance."""
    global _gpuz_bypass
    if _gpuz_bypass is None:
        _gpuz_bypass = GPUZBypass()
    return _gpuz_bypass


if __name__ == "__main__":
    # Test the bypass module
    logging.basicConfig(level=logging.INFO)

    from src.core.config_manager import get_config_manager

    config = get_config_manager()
    profiles = config.list_profiles()

    if profiles:
        # Use RTX 4090 if available
        profile = next((p for p in profiles if "4090" in p.name), profiles[0])
        print(f"\nUsing profile: {profile.name}")

        bypass = get_gpuz_bypass()
        bypass.set_profile(profile)

        print("\n📊 GPU-Z Compatible Data:")
        print("-" * 50)
        gpuz_data = bypass.generate_fake_gpuz_data()
        for key, value in gpuz_data.items():
            print(f"  {key}: {value}")

        print(bypass.get_hook_instructions())
