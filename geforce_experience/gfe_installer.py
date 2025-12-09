"""
GeForce Experience Installer
Installs the fake GeForce Experience as a system app with shortcuts.
Mirrors the pattern from nvidia_panel/installer.py.
"""

import os
import sys
import shutil
import ctypes
import logging
from pathlib import Path
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


def is_windows() -> bool:
    """Return True if running on Windows."""
    return os.name == 'nt' or sys.platform.startswith('win')


def is_admin() -> bool:
    """Check if running as administrator (Windows). Returns False on non-Windows."""
    if not is_windows():
        return False
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def get_install_paths() -> Tuple[Path, Path, Path]:
    """
    Get installation paths for GeForce Experience.
    Returns: (install_dir, start_menu_dir, desktop_path)
    """
    if not is_windows():
        home = Path(os.path.expanduser("~"))
        return (home / "GeForce_Experience_Sim"), (home / "StartMenu"), (home / "Desktop")

    # Program Files path
    program_files = Path(os.environ.get("PROGRAMFILES", "C:/Program Files"))
    install_dir = program_files / "NVIDIA Corporation" / "NVIDIA GeForce Experience"

    # Start Menu path
    appdata = Path(os.environ.get("APPDATA", ""))
    start_menu = appdata / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "NVIDIA Corporation"

    # Desktop path
    desktop = Path(os.path.expanduser("~")) / "Desktop"

    return install_dir, start_menu, desktop


def create_shortcut(target_path: Path, shortcut_path: Path, icon_path: Optional[Path] = None,
                   description: str = "") -> bool:
    """
    Create a Windows shortcut (.lnk) file.
    """
    if not is_windows():
        logger.warning("create_shortcut called on non-Windows platform; skipping.")
        return False
    try:
        import win32com.client

        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(str(shortcut_path))
        shortcut.TargetPath = str(target_path)
        shortcut.WorkingDirectory = str(target_path.parent)
        shortcut.Description = description

        if icon_path and icon_path.exists():
            shortcut.IconLocation = str(icon_path)

        shortcut.save()
        logger.info(f"Created shortcut: {shortcut_path}")
        return True

    except Exception as e:
        logger.error(f"Failed to create shortcut: {e}")
        return False


def install_geforce_experience(source_dir: Path) -> Tuple[bool, str]:
    """
    Install GeForce Experience to Program Files.

    Args:
        source_dir: Path to the geforce_experience source directory

    Returns:
        Tuple of (success, message)
    """
    if not is_windows():
        return False, "Installation is only supported on Windows."
    if not is_admin():
        return False, "Administrator privileges required.\nPlease run GPU-SIM as Administrator."

    install_dir, start_menu, desktop = get_install_paths()

    try:
        # Create installation directory
        install_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created install directory: {install_dir}")

        # Copy all python files
        files_to_copy = [
            "geforce_experience.py",
            "gfe_style.py",
            "__init__.py",
            "gfe_installer.py",
        ]

        tabs_dir = install_dir / "tabs"
        tabs_dir.mkdir(exist_ok=True)

        # Copy main files
        for file_name in files_to_copy:
            src = source_dir / file_name
            if src.exists():
                shutil.copy2(src, install_dir / file_name)

        # Copy tabs
        tabs_src = source_dir / "tabs"
        if tabs_src.exists():
            for tab_file in tabs_src.glob("*.py"):
                shutil.copy2(tab_file, tabs_dir / tab_file.name)

        # Copy src/core (required for profiles)
        src_core_dir = source_dir.parent / "src" / "core"
        if src_core_dir.exists():
            dest_src = install_dir / "src"
            dest_core = dest_src / "core"
            dest_src.mkdir(exist_ok=True)
            dest_core.mkdir(exist_ok=True)

            # Create src/__init__.py
            (dest_src / "__init__.py").write_text("# GPU-SIM src package\n")

            for py_file in src_core_dir.glob("*.py"):
                shutil.copy2(py_file, dest_core / py_file.name)

        # Copy config/gpu_profiles
        config_src = source_dir.parent / "config" / "gpu_profiles"
        if config_src.exists():
            config_dest = install_dir / "config" / "gpu_profiles"
            config_dest.mkdir(parents=True, exist_ok=True)
            for json_file in config_src.glob("*.json"):
                shutil.copy2(json_file, config_dest / json_file.name)

        # Copy icon (use same NVIDIA icon)
        icon_src = source_dir.parent / "Agenda" / "512x512.png"
        if icon_src.exists():
            shutil.copy2(icon_src, install_dir / "gfe_icon.png")

        # Create launcher batch file with proper PYTHONPATH
        launcher_path = install_dir / "GeForce Experience.bat"
        launcher_content = f'''@echo off
cd /d "{install_dir}"
set PYTHONPATH={install_dir}
pythonw geforce_experience.py
'''
        launcher_path.write_text(launcher_content)

        # Create Start Menu shortcut
        start_menu.mkdir(parents=True, exist_ok=True)
        shortcut_path = start_menu / "GeForce Experience.lnk"
        create_shortcut(
            target_path=launcher_path,
            shortcut_path=shortcut_path,
            icon_path=install_dir / "gfe_icon.png",
            description="NVIDIA GeForce Experience"
        )

        # Create Desktop shortcut
        desktop_shortcut = desktop / "GeForce Experience.lnk"
        create_shortcut(
            target_path=launcher_path,
            shortcut_path=desktop_shortcut,
            icon_path=install_dir / "gfe_icon.png",
            description="NVIDIA GeForce Experience"
        )

        return True, f"GeForce Experience installed successfully!\n\n" \
                     f"Location: {install_dir}\n\n" \
                     f"Shortcuts created:\n" \
                     f"• Start Menu\n" \
                     f"• Desktop"

    except PermissionError:
        return False, "Permission denied.\nPlease run as Administrator."
    except Exception as e:
        return False, f"Installation failed:\n{str(e)}"


def uninstall_geforce_experience() -> Tuple[bool, str]:
    """
    Uninstall GeForce Experience.
    """
    if not is_windows():
        return False, "Uninstallation is only supported on Windows."
    if not is_admin():
        return False, "Administrator privileges required."

    install_dir, start_menu, desktop = get_install_paths()

    try:
        # Remove installation directory
        if install_dir.exists():
            shutil.rmtree(install_dir)

        # Remove Start Menu shortcut
        shortcut_path = start_menu / "GeForce Experience.lnk"
        if shortcut_path.exists():
            shortcut_path.unlink()

        # Remove Desktop shortcut
        desktop_shortcut = desktop / "GeForce Experience.lnk"
        if desktop_shortcut.exists():
            desktop_shortcut.unlink()

        return True, "GeForce Experience uninstalled successfully."

    except Exception as e:
        return False, f"Uninstallation failed:\n{str(e)}"


def is_installed() -> bool:
    """Check if GeForce Experience is already installed."""
    if not is_windows():
        return False
    install_dir, _, _ = get_install_paths()
    return (install_dir / "geforce_experience.py").exists()
