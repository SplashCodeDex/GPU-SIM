# GPU-SIM Source Package
from .core.config_manager import get_config_manager, ConfigManager
from .core.gpu_profile import GPUProfile, DisplayMode

__version__ = "1.0.0"
__all__ = ["get_config_manager", "ConfigManager", "GPUProfile", "DisplayMode"]
