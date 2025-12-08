"""
Unit tests for ConfigManager and GPUProfile classes.
"""

import pytest
import json
import tempfile
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.config_manager import ConfigManager
from src.core.gpu_profile import GPUProfile, DisplayMode


class TestDisplayMode:
    """Tests for DisplayMode class."""

    def test_display_mode_creation(self):
        mode = DisplayMode(width=1920, height=1080, refresh=60)
        assert mode.width == 1920
        assert mode.height == 1080
        assert mode.refresh == 60

    def test_display_mode_str(self):
        mode = DisplayMode(width=2560, height=1440, refresh=144)
        assert str(mode) == "2560x1440 @ 144Hz"

    def test_display_mode_to_dict(self):
        mode = DisplayMode(width=3840, height=2160, refresh=60)
        d = mode.to_dict()
        assert d == {"width": 3840, "height": 2160, "refresh": 60}


class TestGPUProfile:
    """Tests for GPUProfile class."""

    def test_profile_creation(self):
        profile = GPUProfile(
            id="test_gpu",
            name="Test GPU",
            manufacturer="Test Corp",
            driver_version="1.0.0"
        )
        assert profile.id == "test_gpu"
        assert profile.name == "Test GPU"

    def test_profile_vram_properties(self):
        profile = GPUProfile(
            id="test",
            name="Test",
            manufacturer="Test",
            driver_version="1.0",
            vram_mb=4096
        )
        assert profile.vram_bytes == 4096 * 1024 * 1024
        assert profile.vram_gb == 4.0

    def test_profile_is_nvidia(self):
        nvidia_profile = GPUProfile(
            id="nvidia",
            name="GeForce",
            manufacturer="NVIDIA Corporation",
            driver_version="1.0"
        )
        assert nvidia_profile.is_nvidia is True
        assert nvidia_profile.is_amd is False

    def test_profile_is_amd(self):
        amd_profile = GPUProfile(
            id="amd",
            name="Radeon",
            manufacturer="Advanced Micro Devices, Inc.",
            driver_version="1.0"
        )
        assert amd_profile.is_nvidia is False
        assert amd_profile.is_amd is True

    def test_profile_compute_units(self):
        nvidia = GPUProfile(
            id="nvidia",
            name="Test",
            manufacturer="NVIDIA",
            driver_version="1.0",
            cuda_cores=8704
        )
        assert nvidia.compute_units == 8704

        amd = GPUProfile(
            id="amd",
            name="Test",
            manufacturer="AMD",
            driver_version="1.0",
            stream_processors=4608
        )
        assert amd.compute_units == 4608

    def test_profile_to_dict(self):
        profile = GPUProfile(
            id="test",
            name="Test GPU",
            manufacturer="Test",
            driver_version="1.0",
            vram_mb=8192
        )
        d = profile.to_dict()
        assert d["id"] == "test"
        assert d["name"] == "Test GPU"
        assert d["vram_mb"] == 8192

    def test_profile_from_dict(self):
        data = {
            "id": "test_gpu",
            "name": "Test GPU",
            "manufacturer": "Test Corp",
            "driver_version": "2.0",
            "vram_mb": 16384,
            "display_modes": [
                {"width": 1920, "height": 1080, "refresh": 60}
            ]
        }
        profile = GPUProfile.from_dict(data)
        assert profile.id == "test_gpu"
        assert profile.vram_mb == 16384
        assert len(profile.display_modes) == 1
        assert profile.display_modes[0].width == 1920

    def test_profile_get_max_resolution(self):
        profile = GPUProfile(
            id="test",
            name="Test",
            manufacturer="Test",
            driver_version="1.0",
            display_modes=[
                DisplayMode(1920, 1080, 60),
                DisplayMode(3840, 2160, 60),
                DisplayMode(2560, 1440, 144),
            ]
        )
        max_res = profile.get_max_resolution()
        assert max_res.width == 3840
        assert max_res.height == 2160


class TestConfigManager:
    """Tests for ConfigManager class."""

    @pytest.fixture
    def temp_profiles_dir(self):
        """Create a temporary directory with test profiles."""
        with tempfile.TemporaryDirectory() as tmpdir:
            profiles_dir = Path(tmpdir) / "profiles"
            profiles_dir.mkdir()

            # Create test profile
            profile_data = {
                "id": "test_profile",
                "name": "Test Profile GPU",
                "manufacturer": "Test Manufacturer",
                "driver_version": "1.0.0",
                "vram_mb": 8192,
                "display_modes": [
                    {"width": 1920, "height": 1080, "refresh": 60}
                ]
            }

            with open(profiles_dir / "test_profile.json", "w") as f:
                json.dump(profile_data, f)

            yield profiles_dir

    def test_load_profiles(self, temp_profiles_dir):
        manager = ConfigManager(profiles_dir=str(temp_profiles_dir))
        count = manager.load_profiles()
        assert count == 1

    def test_get_profile(self, temp_profiles_dir):
        manager = ConfigManager(profiles_dir=str(temp_profiles_dir))
        manager.load_profiles()

        profile = manager.get_profile("test_profile")
        assert profile is not None
        assert profile.name == "Test Profile GPU"

    def test_get_profile_not_found(self, temp_profiles_dir):
        manager = ConfigManager(profiles_dir=str(temp_profiles_dir))
        manager.load_profiles()

        profile = manager.get_profile("nonexistent")
        assert profile is None

    def test_list_profiles(self, temp_profiles_dir):
        manager = ConfigManager(profiles_dir=str(temp_profiles_dir))
        manager.load_profiles()

        profiles = manager.list_profiles()
        assert len(profiles) == 1
        assert profiles[0].id == "test_profile"

    def test_active_profile(self, temp_profiles_dir):
        manager = ConfigManager(profiles_dir=str(temp_profiles_dir))
        manager.load_profiles()

        assert manager.active_profile is None

        profile = manager.get_profile("test_profile")
        manager.active_profile = profile

        assert manager.active_profile is not None
        assert manager.active_profile.id == "test_profile"

    def test_save_profile(self, temp_profiles_dir):
        manager = ConfigManager(profiles_dir=str(temp_profiles_dir))

        new_profile = GPUProfile(
            id="new_profile",
            name="New GPU",
            manufacturer="New Manufacturer",
            driver_version="2.0.0"
        )

        success = manager.save_profile(new_profile)
        assert success is True

        # Verify file was created
        assert (temp_profiles_dir / "new_profile.json").exists()

    def test_delete_profile(self, temp_profiles_dir):
        manager = ConfigManager(profiles_dir=str(temp_profiles_dir))
        manager.load_profiles()

        assert manager.get_profile("test_profile") is not None

        success = manager.delete_profile("test_profile")
        assert success is True

        assert manager.get_profile("test_profile") is None


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
