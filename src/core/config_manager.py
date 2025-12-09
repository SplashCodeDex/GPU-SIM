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
    ACTIVE_PROFILE_FILE = ".gpu_sim_active.json"

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

        # Determine active profile storage location
        self._active_profile_path = Path.home() / self.ACTIVE_PROFILE_FILE

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
        """Set the active profile and persist to disk."""
        self._active_profile = profile
        if profile:
            logger.info(f"Active profile set to: {profile.name}")
            self._save_active_profile_id(profile.id)
        else:
            self._clear_active_profile()

    def _save_active_profile_id(self, profile_id: str) -> None:
        """Save the active profile ID to disk for sharing between apps."""
        try:
            data = {"active_profile_id": profile_id}
            with open(self._active_profile_path, "w", encoding="utf-8") as f:
                json.dump(data, f)
            logger.debug(f"Saved active profile ID to {self._active_profile_path}")
        except Exception as e:
            logger.warning(f"Failed to save active profile ID: {e}")

    def _clear_active_profile(self) -> None:
        """Remove the active profile file."""
        try:
            if self._active_profile_path.exists():
                self._active_profile_path.unlink()
        except Exception as e:
            logger.warning(f"Failed to clear active profile: {e}")

    def load_active_profile(self) -> Optional[GPUProfile]:
        """
        Load the previously active profile from disk.

        This allows NVIDIA Control Panel and GeForce Experience to use
        the same profile that was selected in GPU-SIM.

        Returns:
            The active GPUProfile if found, None otherwise.
        """
        try:
            if not self._active_profile_path.exists():
                return None

            with open(self._active_profile_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            profile_id = data.get("active_profile_id")
            if profile_id and profile_id in self._profiles:
                self._active_profile = self._profiles[profile_id]
                logger.info(f"Loaded active profile: {self._active_profile.name}")
                return self._active_profile

            return None
        except Exception as e:
            logger.warning(f"Failed to load active profile: {e}")
            return None

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

    def export_profile(self, profile_id: str, export_path: Path) -> bool:
        """
        Export a profile to an external JSON file with metadata.

        Args:
            profile_id: The profile identifier to export.
            export_path: Path to save the exported JSON file.

        Returns:
            True if exported successfully, False otherwise.
        """
        profile = self.get_profile(profile_id)
        if not profile:
            logger.error(f"Profile not found: {profile_id}")
            return False

        try:
            from datetime import datetime

            # Create export data with metadata
            export_data = {
                "_export_metadata": {
                    "export_version": "1.0",
                    "export_date": datetime.now().isoformat(),
                    "source_app": "GPU-SIM",
                    "original_id": profile.id,
                },
                **profile.to_dict()
            }

            # Ensure parent directory exists
            export_path.parent.mkdir(parents=True, exist_ok=True)

            with open(export_path, "w", encoding="utf-8") as f:
                json.dump(export_data, f, indent=4)

            logger.info(f"Exported profile '{profile.name}' to {export_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to export profile: {e}")
            return False

    def import_profile(self, import_path: Path, overwrite: bool = False) -> Optional[GPUProfile]:
        """
        Import a profile from an external JSON file.

        Args:
            import_path: Path to the JSON file to import.
            overwrite: Whether to overwrite if profile ID already exists.

        Returns:
            GPUProfile if imported successfully, None otherwise.
        """
        if not import_path.exists():
            logger.error(f"Import file does not exist: {import_path}")
            return None

        try:
            with open(import_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Remove export metadata if present (not part of profile)
            metadata = data.pop("_export_metadata", None)
            if metadata:
                logger.info(f"Importing profile from GPU-SIM export (v{metadata.get('export_version', '?')})")

            # Validate required fields
            if "id" not in data or "name" not in data:
                logger.error("Import file missing required fields: 'id' and 'name'")
                return None

            # Check for ID collision
            profile_id = data["id"]
            if profile_id in self._profiles and not overwrite:
                # Generate a unique ID by appending suffix
                import uuid
                new_id = f"{profile_id}_{uuid.uuid4().hex[:8]}"
                logger.warning(f"Profile ID collision: '{profile_id}' -> '{new_id}'")
                data["id"] = new_id

            # Create profile from data
            profile = GPUProfile.from_dict(data)

            # Save to profiles directory
            if self.save_profile(profile, overwrite=overwrite):
                logger.info(f"Imported profile: {profile.name}")
                return profile
            else:
                logger.error("Failed to save imported profile")
                return None

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in import file: {e}")
            return None
        except KeyError as e:
            logger.error(f"Missing required field in import file: {e}")
            return None
        except Exception as e:
            logger.error(f"Failed to import profile: {e}")
            return None

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
