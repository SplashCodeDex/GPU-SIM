"""
Registry Backup Manager
Provides functionality to backup and restore Windows registry keys.
"""

import os
import logging
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, List

logger = logging.getLogger(__name__)


class BackupManager:
    """
    Manages registry backups for safe modifications.
    Creates timestamped backups and provides restore functionality.
    """

    # Registry paths related to GPU/Display
    GPU_REGISTRY_PATHS = [
        r"HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Video",
        r"HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}",
        r"HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\GraphicsDrivers",
    ]

    def __init__(self, backup_dir: Optional[str] = None):
        """
        Initialize the backup manager.

        Args:
            backup_dir: Directory to store backups. Defaults to 'backups/' in project root.
        """
        if backup_dir:
            self._backup_dir = Path(backup_dir)
        else:
            project_root = Path(__file__).parent.parent.parent
            self._backup_dir = project_root / "backups"

        # Ensure backup directory exists
        self._backup_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"BackupManager initialized with backup dir: {self._backup_dir}")

    @property
    def backup_dir(self) -> Path:
        """Get the backup directory path."""
        return self._backup_dir

    def _generate_backup_filename(self, prefix: str = "gpu_registry") -> str:
        """Generate a timestamped backup filename."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{timestamp}.reg"

    def create_backup(self, registry_path: str, backup_name: Optional[str] = None) -> Optional[Path]:
        """
        Create a backup of a specific registry path.

        Args:
            registry_path: Full registry path to backup (e.g., HKEY_LOCAL_MACHINE\\...)
            backup_name: Optional custom backup filename.

        Returns:
            Path to the backup file if successful, None otherwise.
        """
        if backup_name:
            filename = backup_name if backup_name.endswith(".reg") else f"{backup_name}.reg"
        else:
            # Create safe filename from registry path
            safe_name = registry_path.replace("\\", "_").replace("{", "").replace("}", "")
            filename = self._generate_backup_filename(safe_name[:50])

        backup_path = self._backup_dir / filename

        try:
            # Use reg.exe to export the registry key
            cmd = ["reg", "export", registry_path, str(backup_path), "/y"]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                shell=True
            )

            if result.returncode == 0:
                logger.info(f"Created backup: {backup_path}")
                return backup_path
            else:
                logger.error(f"Failed to create backup: {result.stderr}")
                return None

        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            return None

    def create_full_gpu_backup(self) -> List[Path]:
        """
        Create backups of all GPU-related registry paths.

        Returns:
            List of paths to created backup files.
        """
        backups = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        for registry_path in self.GPU_REGISTRY_PATHS:
            # Create safe filename
            path_name = registry_path.split("\\")[-1][:30]
            backup_name = f"gpu_{path_name}_{timestamp}.reg"

            backup_path = self.create_backup(registry_path, backup_name)
            if backup_path:
                backups.append(backup_path)

        logger.info(f"Created {len(backups)} GPU registry backups")
        return backups

    def restore_backup(self, backup_path: Path) -> bool:
        """
        Restore a registry backup.

        Args:
            backup_path: Path to the .reg backup file.

        Returns:
            True if restored successfully, False otherwise.
        """
        if not backup_path.exists():
            logger.error(f"Backup file not found: {backup_path}")
            return False

        try:
            # Use reg.exe to import the registry file
            cmd = ["reg", "import", str(backup_path)]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                shell=True
            )

            if result.returncode == 0:
                logger.info(f"Restored backup: {backup_path}")
                return True
            else:
                logger.error(f"Failed to restore backup: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"Error restoring backup: {e}")
            return False

    def list_backups(self) -> List[Path]:
        """
        List all available backup files.

        Returns:
            List of paths to backup files, sorted by modification time (newest first).
        """
        backups = list(self._backup_dir.glob("*.reg"))
        backups.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        return backups

    def get_latest_backup(self, prefix: str = "") -> Optional[Path]:
        """
        Get the most recent backup file.

        Args:
            prefix: Optional prefix to filter backups.

        Returns:
            Path to the latest backup file, or None if no backups exist.
        """
        backups = self.list_backups()
        if prefix:
            backups = [b for b in backups if b.name.startswith(prefix)]
        return backups[0] if backups else None

    def cleanup_old_backups(self, keep_count: int = 10) -> int:
        """
        Remove old backup files, keeping the most recent ones.

        Args:
            keep_count: Number of backups to keep.

        Returns:
            Number of backups deleted.
        """
        backups = self.list_backups()
        to_delete = backups[keep_count:]

        deleted = 0
        for backup in to_delete:
            try:
                backup.unlink()
                deleted += 1
                logger.debug(f"Deleted old backup: {backup}")
            except Exception as e:
                logger.error(f"Failed to delete backup {backup}: {e}")

        logger.info(f"Cleaned up {deleted} old backups")
        return deleted


# Singleton instance
_backup_manager: Optional[BackupManager] = None


def get_backup_manager() -> BackupManager:
    """Get the global BackupManager instance."""
    global _backup_manager
    if _backup_manager is None:
        _backup_manager = BackupManager()
    return _backup_manager
