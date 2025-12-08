"""
Configuration Manager
Handles loading, saving, and managing GPU profiles from JSON files.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

from .gpu_profile import GPUProfile

logger = logging.getLogger(__name__)


class ConfigManager:
    """
    Manages GPU profile configurations.
    Loads profiles from JSON files and provides access to them.
    """

    DEFAULT_PROFILES_DIR = "config/gpu_profiles"

    def __init__(self, profiles_dir: Optional[str] = None):
        """
        Initialize the configuration manager.

        Args:
            profiles_dir: Path to the GPU profiles directory.
                         If None, uses the default location.
        """
        self._profiles: Dict[str, GPUProfile] = {}
        self._active_profile: Optional[GPUProfile] = None

        # Determine profiles directory
        if profiles_dir:
            self._profiles_dir = Path(profiles_dir)
        else:
            # Use path relative to project root
            project_root = Path(__file__).parent.parent.parent
            self._profiles_dir = project_root / self.DEFAULT_PROFILES_DIR

        logger.info(f"ConfigManager initialized with profiles dir: {self._profiles_dir}")

    @property
    def profiles_dir(self) -> Path:
        """Get the profiles directory path."""
        return self._profiles_dir

    @property
    def profiles(self) -> Dict[str, GPUProfile]:
        """Get all loaded profiles."""
        return self._profiles.copy()

    @property
    def active_profile(self) -> Optional[GPUProfile]:
        """Get the currently active profile."""
        return self._active_profile

    @active_profile.setter
    def active_profile(self, profile: Optional[GPUProfile]) -> None:
        """Set the active profile."""
        self._active_profile = profile
        if profile:
            logger.info(f"Active profile set to: {profile.name}")

    def load_profiles(self) -> int:
        """
        Load all GPU profiles from the profiles directory.

        Returns:
            Number of profiles loaded.
        """
        self._profiles.clear()

        if not self._profiles_dir.exists():
            logger.warning(f"Profiles directory does not exist: {self._profiles_dir}")
            return 0

        loaded = 0
        for file_path in self._profiles_dir.glob("*.json"):
            try:
                profile = self._load_profile_file(file_path)
                if profile:
                    self._profiles[profile.id] = profile
                    loaded += 1
                    logger.debug(f"Loaded profile: {profile.name}")
            except Exception as e:
                logger.error(f"Failed to load profile from {file_path}: {e}")

        logger.info(f"Loaded {loaded} GPU profiles")
        return loaded

    def _load_profile_file(self, file_path: Path) -> Optional[GPUProfile]:
        """
        Load a single profile from a JSON file.

        Args:
            file_path: Path to the JSON file.

        Returns:
            GPUProfile if successful, None otherwise.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return GPUProfile.from_dict(data)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {file_path}: {e}")
            return None
        except KeyError as e:
            logger.error(f"Missing required field in {file_path}: {e}")
            return None

    def get_profile(self, profile_id: str) -> Optional[GPUProfile]:
        """
        Get a profile by its ID.

        Args:
            profile_id: The profile identifier.

        Returns:
            GPUProfile if found, None otherwise.
        """
        return self._profiles.get(profile_id)

    def get_profile_by_name(self, name: str) -> Optional[GPUProfile]:
        """
        Get a profile by its display name.

        Args:
            name: The profile display name.

        Returns:
            GPUProfile if found, None otherwise.
        """
        for profile in self._profiles.values():
            if profile.name.lower() == name.lower():
                return profile
        return None

    def list_profiles(self) -> List[GPUProfile]:
        """
        Get a list of all loaded profiles.

        Returns:
            List of GPUProfile objects.
        """
        return list(self._profiles.values())

    def save_profile(self, profile: GPUProfile, overwrite: bool = False) -> bool:
        """
        Save a profile to a JSON file.

        Args:
            profile: The GPUProfile to save.
            overwrite: Whether to overwrite existing file.

        Returns:
            True if saved successfully, False otherwise.
        """
        file_path = self._profiles_dir / f"{profile.id}.json"

        if file_path.exists() and not overwrite:
            logger.warning(f"Profile file already exists: {file_path}")
            return False

        try:
            # Ensure directory exists
            self._profiles_dir.mkdir(parents=True, exist_ok=True)

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(profile.to_dict(), f, indent=4)

            # Add to loaded profiles
            self._profiles[profile.id] = profile
            logger.info(f"Saved profile: {profile.name}")
            return True

        except Exception as e:
            logger.error(f"Failed to save profile: {e}")
            return False

    def delete_profile(self, profile_id: str) -> bool:
        """
        Delete a profile.

        Args:
            profile_id: The profile identifier to delete.

        Returns:
            True if deleted successfully, False otherwise.
        """
        file_path = self._profiles_dir / f"{profile_id}.json"

        try:
            if file_path.exists():
                file_path.unlink()

            if profile_id in self._profiles:
                del self._profiles[profile_id]

            # Clear active profile if deleted
            if self._active_profile and self._active_profile.id == profile_id:
                self._active_profile = None

            logger.info(f"Deleted profile: {profile_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to delete profile: {e}")
            return False

    def get_nvidia_profiles(self) -> List[GPUProfile]:
        """Get all NVIDIA profiles."""
        return [p for p in self._profiles.values() if p.is_nvidia]

    def get_amd_profiles(self) -> List[GPUProfile]:
        """Get all AMD profiles."""
        return [p for p in self._profiles.values() if p.is_amd]


# Singleton instance
_config_manager: Optional[ConfigManager] = None


def get_config_manager() -> ConfigManager:
    """
    Get the global ConfigManager instance.

    Returns:
        The singleton ConfigManager instance.
    """
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
        _config_manager.load_profiles()
    return _config_manager
