"""
Test suite for GPU-SIM UI components.
Tests Home Panel, Installer Wizard, and Verification Panel.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestHomePanel:
    """Tests for HomePanel functionality."""

    def test_home_panel_import(self):
        """Test that HomePanel can be imported."""
        from src.ui.panels.home_panel import HomePanel
        assert HomePanel is not None

    def test_stat_card_import(self):
        """Test that StatCard can be imported."""
        from src.ui.panels.home_panel import StatCard
        assert StatCard is not None

    @patch('src.ui.panels.home_panel.QWidget')
    def test_home_panel_has_gpuz_bypass(self, mock_widget):
        """Test that HomePanel has GPU-Z bypass toggle."""
        from src.ui.panels.home_panel import HomePanel
        assert hasattr(HomePanel, '_on_gpuz_bypass_toggled')


class TestInstallerWizard:
    """Tests for InstallerWizard functionality."""

    def test_installer_wizard_import(self):
        """Test that InstallerWizard can be imported."""
        from src.ui.installer_wizard import InstallerWizard
        assert InstallerWizard is not None

    def test_install_worker_import(self):
        """Test that InstallWorker can be imported."""
        from src.ui.installer_wizard import InstallWorker
        assert InstallWorker is not None

    def test_wizard_pages_import(self):
        """Test that wizard page classes can be imported."""
        from src.ui.installer_wizard import (
            WelcomePage, ConfigPage, ComponentsPage,
            InstallPage, CompletePage
        )
        assert WelcomePage is not None
        assert ConfigPage is not None
        assert ComponentsPage is not None
        assert InstallPage is not None
        assert CompletePage is not None


class TestVerificationPanel:
    """Tests for VerificationPanel functionality."""

    def test_verification_panel_import(self):
        """Test that VerificationPanel can be imported."""
        from src.ui.panels.verification_panel import VerificationPanel
        assert VerificationPanel is not None

    def test_verification_step_import(self):
        """Test that VerificationStep can be imported."""
        from src.ui.panels.verification_panel import VerificationStep
        assert VerificationStep is not None

    def test_verification_step_has_actions(self):
        """Test that VerificationStep has action methods."""
        from src.ui.panels.verification_panel import VerificationStep
        assert hasattr(VerificationStep, '_on_action')
        assert hasattr(VerificationStep, '_launch_nvidia_panel')


class TestGPUProfiles:
    """Tests for GPU profile loading."""

    def test_all_profiles_valid_json(self):
        """Test that all GPU profile JSON files are valid."""
        import json
        profile_dir = project_root / "config" / "gpu_profiles"

        for json_file in profile_dir.glob("*.json"):
            with open(json_file, 'r') as f:
                data = json.load(f)
                assert 'id' in data, f"Missing 'id' in {json_file.name}"
                assert 'name' in data, f"Missing 'name' in {json_file.name}"
                assert 'vram_mb' in data, f"Missing 'vram_mb' in {json_file.name}"

    def test_profile_count(self):
        """Test that we have expected number of profiles."""
        profile_dir = project_root / "config" / "gpu_profiles"
        profiles = list(profile_dir.glob("*.json"))
        assert len(profiles) >= 12, f"Expected 12+ profiles, got {len(profiles)}"

    def test_new_profiles_exist(self):
        """Test that newly added profiles exist."""
        profile_dir = project_root / "config" / "gpu_profiles"
        expected_new = [
            "nvidia_rtx_4060.json",
            "nvidia_rtx_3060.json",
            "nvidia_gtx_1080ti.json"
        ]
        for profile in expected_new:
            assert (profile_dir / profile).exists(), f"Missing profile: {profile}"


class TestVDDInstaller:
    """Tests for VDD installer module."""

    def test_vdd_installer_import(self):
        """Test that VDD installer can be imported."""
        from src.vdd.vdd_installer import VDDInstaller
        assert VDDInstaller is not None

    def test_is_admin_function(self):
        """Test that is_admin function exists."""
        from src.vdd.vdd_installer import is_admin
        assert callable(is_admin)

    def test_is_test_signing_function(self):
        """Test that is_test_signing_enabled function exists."""
        from src.vdd.vdd_installer import is_test_signing_enabled
        assert callable(is_test_signing_enabled)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
