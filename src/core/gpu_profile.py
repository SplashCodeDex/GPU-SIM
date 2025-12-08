"""
GPU Profile Data Class
Represents a virtual GPU configuration with all specifications and registry entries.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any


@dataclass
class DisplayMode:
    """Represents a display mode (resolution + refresh rate)."""
    width: int
    height: int
    refresh: int

    def __str__(self) -> str:
        return f"{self.width}x{self.height} @ {self.refresh}Hz"

    def to_dict(self) -> Dict[str, int]:
        return {"width": self.width, "height": self.height, "refresh": self.refresh}


@dataclass
class GPUProfile:
    """
    Complete GPU profile containing all specifications needed for simulation.
    """
    # Identification
    id: str
    name: str
    manufacturer: str

    # Driver info
    driver_version: str
    driver_date: str = ""

    # Memory
    vram_mb: int = 0
    vram_type: str = "GDDR5"

    # Clock speeds
    base_clock_mhz: int = 0
    boost_clock_mhz: int = 0
    memory_clock_mhz: int = 0
    memory_bus_width: int = 256

    # Power
    tdp_watts: int = 0

    # Compute units (NVIDIA=CUDA cores, AMD=Stream processors)
    cuda_cores: int = 0
    stream_processors: int = 0

    # PCI IDs
    pci_device_id: str = ""
    pci_vendor_id: str = ""
    subsystem_id: str = ""

    # Display info
    device_description: str = ""
    video_processor: str = ""
    dac_type: str = "Integrated RAMDAC"
    adapter_compatibility: str = ""

    # Registry entries to create
    registry_entries: Dict[str, Any] = field(default_factory=dict)

    # Supported display modes
    display_modes: List[DisplayMode] = field(default_factory=list)

    # Additional features
    features: Dict[str, Any] = field(default_factory=dict)

    @property
    def vram_bytes(self) -> int:
        """Get VRAM in bytes."""
        return self.vram_mb * 1024 * 1024

    @property
    def vram_gb(self) -> float:
        """Get VRAM in GB."""
        return self.vram_mb / 1024

    @property
    def compute_units(self) -> int:
        """Get compute units (CUDA cores or stream processors)."""
        return self.cuda_cores or self.stream_processors

    @property
    def is_nvidia(self) -> bool:
        """Check if this is an NVIDIA GPU."""
        return "NVIDIA" in self.manufacturer.upper()

    @property
    def is_amd(self) -> bool:
        """Check if this is an AMD GPU."""
        return "AMD" in self.manufacturer.upper() or "ATI" in self.manufacturer.upper()

    def get_max_resolution(self) -> Optional[DisplayMode]:
        """Get the highest supported resolution."""
        if not self.display_modes:
            return None
        return max(self.display_modes, key=lambda m: m.width * m.height)

    def to_dict(self) -> Dict[str, Any]:
        """Convert profile to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "manufacturer": self.manufacturer,
            "driver_version": self.driver_version,
            "driver_date": self.driver_date,
            "vram_mb": self.vram_mb,
            "vram_type": self.vram_type,
            "cuda_cores": self.cuda_cores,
            "stream_processors": self.stream_processors,
            "base_clock_mhz": self.base_clock_mhz,
            "boost_clock_mhz": self.boost_clock_mhz,
            "memory_clock_mhz": self.memory_clock_mhz,
            "memory_bus_width": self.memory_bus_width,
            "tdp_watts": self.tdp_watts,
            "pci_device_id": self.pci_device_id,
            "pci_vendor_id": self.pci_vendor_id,
            "subsystem_id": self.subsystem_id,
            "device_description": self.device_description,
            "video_processor": self.video_processor,
            "dac_type": self.dac_type,
            "adapter_compatibility": self.adapter_compatibility,
            "registry_entries": self.registry_entries,
            "display_modes": [m.to_dict() for m in self.display_modes],
            "features": self.features,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GPUProfile":
        """Create GPUProfile from dictionary."""
        # Parse display modes
        display_modes = []
        for mode in data.get("display_modes", []):
            display_modes.append(DisplayMode(
                width=mode["width"],
                height=mode["height"],
                refresh=mode["refresh"]
            ))

        return cls(
            id=data.get("id", ""),
            name=data.get("name", "Unknown GPU"),
            manufacturer=data.get("manufacturer", "Unknown"),
            driver_version=data.get("driver_version", "1.0.0"),
            driver_date=data.get("driver_date", ""),
            vram_mb=data.get("vram_mb", 0),
            vram_type=data.get("vram_type", "GDDR5"),
            cuda_cores=data.get("cuda_cores", 0),
            stream_processors=data.get("stream_processors", 0),
            base_clock_mhz=data.get("base_clock_mhz", 0),
            boost_clock_mhz=data.get("boost_clock_mhz", 0),
            memory_clock_mhz=data.get("memory_clock_mhz", 0),
            memory_bus_width=data.get("memory_bus_width", 256),
            tdp_watts=data.get("tdp_watts", 0),
            pci_device_id=data.get("pci_device_id", ""),
            pci_vendor_id=data.get("pci_vendor_id", ""),
            subsystem_id=data.get("subsystem_id", ""),
            device_description=data.get("device_description", data.get("name", "")),
            video_processor=data.get("video_processor", ""),
            dac_type=data.get("dac_type", "Integrated RAMDAC"),
            adapter_compatibility=data.get("adapter_compatibility", ""),
            registry_entries=data.get("registry_entries", {}),
            display_modes=display_modes,
            features=data.get("features", {}),
        )

    def __str__(self) -> str:
        return f"{self.name} ({self.vram_gb:.0f}GB)"

    def __repr__(self) -> str:
        return f"GPUProfile(id='{self.id}', name='{self.name}')"
