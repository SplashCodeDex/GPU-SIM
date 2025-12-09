"""
Detection Bypass Module
Comprehensive GPU detection bypass for GPU-Z, Speccy, HWiNFO, and other tools.

This module consolidates all detection spoofing methods:
- WMI (Win32_VideoController) - Primary Windows detection
- Registry spoofing - HKLM display adapter keys
- NVAPI shims - NVIDIA SDK bypass
- ADL shims - AMD SDK bypass
- DirectX DXGI - DirectX adapter enumeration
"""

import logging
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.gpu_profile import GPUProfile

logger = logging.getLogger(__name__)


@dataclass
class BypassStatus:
    """Status of individual bypass methods."""
    name: str
    status: str  # "active", "partial", "unavailable"
    icon: str    # "✅", "⚠️", "❌"
    description: str


class DetectionBypass:
    """
    Consolidated manager for GPU detection tool bypass.

    Detection Tools & Their Methods:
    ✅ Registry           - Covered by gpu_registry module
    ✅ WMI                 - Win32_VideoController spoofing
    ⚠️ NVAPI              - Partial bypass via registry shims
    ⚠️ ADL                - Partial bypass via registry shims
    ⚠️ DirectX DXGI       - Handled by gpuz_bypass module
    ❌ Direct PCI         - Requires kernel driver (not implemented)
    """

    # NVIDIA vendor ID
    VENDOR_NVIDIA = 0x10DE
    # AMD vendor ID
    VENDOR_AMD = 0x1002
    # Intel vendor ID
    VENDOR_INTEL = 0x8086

    def __init__(self, profile: Optional[GPUProfile] = None):
        self._profile = profile
        self._bypass_active = False

    def set_profile(self, profile: GPUProfile) -> None:
        """Set the GPU profile to spoof."""
        self._profile = profile
        logger.info(f"Detection bypass profile set: {profile.name}")

    def get_bypass_status(self) -> List[BypassStatus]:
        """Get status of all bypass methods."""
        statuses = [
            BypassStatus(
                name="Registry",
                status="active" if self._profile else "unavailable",
                icon="✅" if self._profile else "❌",
                description="Display adapter registry keys"
            ),
            BypassStatus(
                name="WMI",
                status="active" if self._profile else "unavailable",
                icon="✅" if self._profile else "❌",
                description="Win32_VideoController class"
            ),
            BypassStatus(
                name="NVAPI",
                status="partial" if self._profile and self._profile.is_nvidia else "unavailable",
                icon="⚠️" if self._profile and self._profile.is_nvidia else "❌",
                description="NVIDIA API (registry shims only)"
            ),
            BypassStatus(
                name="ADL",
                status="partial" if self._profile and self._profile.is_amd else "unavailable",
                icon="⚠️" if self._profile and self._profile.is_amd else "❌",
                description="AMD Display Library (registry shims only)"
            ),
            BypassStatus(
                name="DirectX DXGI",
                status="partial" if self._profile else "unavailable",
                icon="⚠️" if self._profile else "❌",
                description="DXGI adapter enumeration"
            ),
            BypassStatus(
                name="Direct PCI",
                status="unavailable",
                icon="❌",
                description="Requires kernel driver"
            ),
        ]
        return statuses

    def generate_wmi_data(self) -> Dict[str, Any]:
        """
        Generate WMI Win32_VideoController data from profile.

        This data can be used to:
        1. Display what detection tools will see
        2. Create WMI provider override scripts (advanced)
        """
        if not self._profile:
            return {}

        p = self._profile

        # Generate defaults first
        defaults = {
            "Name": p.name,
            "Description": p.name,
            "VideoProcessor": p.video_processor or p.name,
            "AdapterRAM": p.vram_bytes,
            "AdapterDACType": p.dac_type,
            "DriverVersion": p.driver_version,
            "DriverDate": p.driver_date,
            "AdapterCompatibility": p.adapter_compatibility or p.manufacturer,
            "VideoModeDescription": f"1920 x 1080 x 4294967296 colors",
            "Status": "OK",
            "PNPDeviceID": self._generate_pnp_id(),
            "DeviceID": f"VideoController1",
        }

        # Override with profile's wmi_data if available
        if p.wmi_data:
            defaults.update(p.wmi_data)

        return defaults

    def generate_nvapi_data(self) -> Dict[str, Any]:
        """
        Generate NVIDIA NVAPI-compatible data from profile.

        NOTE: Full NVAPI bypass requires DLL injection.
        This generates registry shim values only.
        """
        if not self._profile or not self._profile.is_nvidia:
            return {}

        p = self._profile

        # Determine architecture from GPU name
        arch = "Ada Lovelace"
        if "780" in p.name or "750" in p.name:
            arch = "Kepler"
        elif "980" in p.name or "970" in p.name:
            arch = "Maxwell"
        elif "1080" in p.name or "1070" in p.name:
            arch = "Pascal"
        elif "2080" in p.name or "2070" in p.name:
            arch = "Turing"
        elif "3080" in p.name or "3070" in p.name or "3090" in p.name:
            arch = "Ampere"
        elif "4080" in p.name or "4070" in p.name or "4090" in p.name:
            arch = "Ada Lovelace"

        # Generate defaults first
        defaults = {
            "gpu_name": p.name,
            "gpu_type": "DISCRETE",
            "architecture": arch,
            "bus_type": "PCI Express x16 Gen4" if "40" in p.name else "PCI Express x16 Gen3",
            "vram_size_kb": p.vram_mb * 1024,
            "vram_type": p.vram_type,
            "vram_bus_width": p.memory_bus_width,
            "cuda_cores": p.cuda_cores,
            "base_clock_khz": p.base_clock_mhz * 1000,
            "boost_clock_khz": p.boost_clock_mhz * 1000,
            "memory_clock_khz": p.memory_clock_mhz * 1000,
            "tdp_watts": p.tdp_watts,
            "thermal_limit_c": 83 if "40" in p.name else 90,
            "power_limit_percent": 100,
            "driver_version": p.driver_version,
            "bios_version": p.registry_entries.get("HardwareInformation.BiosString", "Unknown"),
            "ray_tracing": p.features.get("ray_tracing", False),
            "dlss": p.features.get("dlss", False),
            "nvenc": p.features.get("nvenc", True),
        }

        # Override with profile's nvapi_data if available
        if p.nvapi_data:
            defaults.update(p.nvapi_data)

        return defaults

    def generate_adl_data(self) -> Dict[str, Any]:
        """
        Generate AMD ADL-compatible data from profile.

        NOTE: Full ADL bypass requires DLL injection.
        This generates registry shim values only.
        """
        if not self._profile or not self._profile.is_amd:
            return {}

        p = self._profile

        # Determine architecture from GPU name
        arch = "RDNA 3"
        if "6800" in p.name or "6900" in p.name:
            arch = "RDNA 2"
        elif "5700" in p.name or "5600" in p.name:
            arch = "RDNA"
        elif "580" in p.name or "570" in p.name:
            arch = "Polaris"

        # Generate defaults first
        defaults = {
            "adapter_name": p.name,
            "adapter_type": "DISCRETE",
            "architecture": arch,
            "bus_type": "PCI Express x16 Gen4",
            "memory_size_mb": p.vram_mb,
            "memory_type": p.vram_type,
            "memory_bus_width": p.memory_bus_width,
            "stream_processors": p.stream_processors,
            "core_clock_mhz": p.base_clock_mhz,
            "boost_clock_mhz": p.boost_clock_mhz,
            "memory_clock_mhz": p.memory_clock_mhz,
            "tdp_watts": p.tdp_watts,
            "driver_version": p.driver_version,
            "bios_version": p.registry_entries.get("HardwareInformation.BiosString", "Unknown"),
            "ray_tracing": p.features.get("ray_tracing", False),
            "fsr": True,  # All RDNA GPUs support FSR
        }

        # Override with profile's adl_data if available
        if p.adl_data:
            defaults.update(p.adl_data)

        return defaults

    def generate_speccy_data(self) -> Dict[str, Any]:
        """
        Generate data in Speccy-compatible format.
        Speccy reads from WMI and Registry primarily.
        """
        if not self._profile:
            return {}

        p = self._profile

        return {
            "Manufacturer": p.manufacturer,
            "Model": p.name,
            "Device ID": self._generate_device_id_string(),
            "Revision": "A1",
            "Driver Version": p.driver_version,
            "Driver Date": p.driver_date,
            "Memory": f"{p.vram_mb} MB",
            "Memory Type": p.vram_type,
            "Bus Width": f"{p.memory_bus_width}-bit",
            "Current Resolution": "1920 x 1080 @ 60 Hz",
            "DAC Type": p.dac_type,
        }

    def generate_hwinfo_data(self) -> Dict[str, Any]:
        """
        Generate data in HWiNFO-compatible format.
        HWiNFO reads from multiple sources including SMBios.
        """
        if not self._profile:
            return {}

        p = self._profile

        return {
            "GPU": p.name,
            "GPU Codename": p.registry_entries.get("HardwareInformation.ChipType", "Unknown"),
            "Vendor": p.manufacturer,
            "Subvendor": p.manufacturer,
            "Device ID": self._generate_device_id_string(),
            "VRAM Size": f"{p.vram_mb} MB",
            "VRAM Type": p.vram_type,
            "VRAM Bus Width": f"{p.memory_bus_width} bit",
            "GPU Clock (Base)": f"{p.base_clock_mhz} MHz",
            "GPU Clock (Boost)": f"{p.boost_clock_mhz} MHz",
            "Memory Clock": f"{p.memory_clock_mhz} MHz",
            "Shader Units": p.cuda_cores or p.stream_processors,
            "TDP": f"{p.tdp_watts} W",
            "Driver Version": p.driver_version,
            "BIOS Version": p.registry_entries.get("HardwareInformation.BiosString", "Unknown"),
        }

    def _generate_pnp_id(self) -> str:
        """Generate a PNP device ID string."""
        if not self._profile:
            return ""

        # Use hardware_ids if available
        if self._profile.hardware_ids and "pnp_id" in self._profile.hardware_ids:
            return self._profile.hardware_ids["pnp_id"]

        # Generate from vendor/device IDs
        vendor = self._profile.pci_vendor_id or "10DE"
        device_id = self._profile.pci_device_id or "0000"

        # Handle format like "10DE-2684"
        if "-" in device_id:
            parts = device_id.split("-")
            if len(parts) == 2:
                vendor = parts[0]
                device_id = parts[1]

        return f"PCI\\VEN_{vendor}&DEV_{device_id}&SUBSYS_00000000&REV_A1"

    def _generate_device_id_string(self) -> str:
        """Generate device ID string in standard format."""
        if not self._profile:
            return "0x0000"

        vendor = self._profile.pci_vendor_id or "10DE"
        device = "0000"

        if self._profile.pci_device_id:
            if "-" in self._profile.pci_device_id:
                parts = self._profile.pci_device_id.split("-")
                device = parts[1] if len(parts) == 2 else parts[0]
            else:
                device = self._profile.pci_device_id

        return f"0x{vendor} / 0x{device}"

    def get_registry_entries(self) -> Dict[str, Any]:
        """
        Get registry entries needed for detection bypass.

        Returns entries for:
        - HKLM\\SYSTEM\\CurrentControlSet\\Control\\Class\\{4d36e968-e325-11ce-bfc1-08002be10318}
        """
        if not self._profile:
            return {}

        p = self._profile
        entries = p.registry_entries.copy() if p.registry_entries else {}

        # Add standard entries if not present
        if "DriverDesc" not in entries:
            entries["DriverDesc"] = p.name
        if "HardwareInformation.AdapterString" not in entries:
            entries["HardwareInformation.AdapterString"] = p.name
        if "HardwareInformation.MemorySize" not in entries:
            entries["HardwareInformation.MemorySize"] = p.vram_bytes
        if "ProviderName" not in entries:
            entries["ProviderName"] = p.manufacturer

        return entries

    def print_bypass_summary(self) -> None:
        """Print a summary of bypass status to console."""
        print("\n" + "=" * 60)
        print("GPU DETECTION BYPASS STATUS")
        print("=" * 60)

        if self._profile:
            print(f"\nActive Profile: {self._profile.name}")
            print(f"Manufacturer: {self._profile.manufacturer}")
            print(f"VRAM: {self._profile.vram_mb} MB")
        else:
            print("\nNo profile active!")

        print("\n" + "-" * 40)
        print("Bypass Methods:")

        for status in self.get_bypass_status():
            print(f"  {status.icon} {status.name:<15} [{status.status}]")
            print(f"      {status.description}")

        print("\n" + "=" * 60)


# Singleton
_detection_bypass: Optional[DetectionBypass] = None


def get_detection_bypass() -> DetectionBypass:
    """Get the singleton detection bypass instance."""
    global _detection_bypass
    if _detection_bypass is None:
        _detection_bypass = DetectionBypass()
    return _detection_bypass


if __name__ == "__main__":
    # Test the module
    logging.basicConfig(level=logging.INFO)

    from src.core.config_manager import get_config_manager

    config = get_config_manager()
    profiles = config.list_profiles()

    if profiles:
        # Use RTX 4090 if available, otherwise first NVIDIA
        profile = next(
            (p for p in profiles if "4090" in p.name),
            next((p for p in profiles if p.is_nvidia), profiles[0])
        )

        bypass = get_detection_bypass()
        bypass.set_profile(profile)
        bypass.print_bypass_summary()

        print("\n📊 WMI Data:")
        for k, v in bypass.generate_wmi_data().items():
            print(f"  {k}: {v}")

        if profile.is_nvidia:
            print("\n🟢 NVAPI Data:")
            for k, v in bypass.generate_nvapi_data().items():
                print(f"  {k}: {v}")

        print("\n🔍 Speccy Data:")
        for k, v in bypass.generate_speccy_data().items():
            print(f"  {k}: {v}")

        print("\n📈 HWiNFO Data:")
        for k, v in bypass.generate_hwinfo_data().items():
            print(f"  {k}: {v}")
