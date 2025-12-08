"""
NVIDIA Control Panel Installer
Installs the fake NVIDIA Control Panel as a system app with shortcuts.
"""

import os
import sys
import shutil
import ctypes
import logging
from pathlib import Path
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


def is_admin() -> bool:
    """Check if running as administrator."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def get_install_paths() -> Tuple[Path, Path, Path]:
    """
    Get installation paths.
    Returns: (install_dir, start_menu_dir, desktop_path)
    """
    # Program Files path
    program_files = Path(os.environ.get("PROGRAMFILES", "C:/Program Files"))
    install_dir = program_files / "NVIDIA Corporation" / "Control Panel"

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


def install_nvidia_control_panel(source_dir: Path) -> Tuple[bool, str]:
    """
    Install the NVIDIA Control Panel to Program Files.

    Args:
        source_dir: Path to the nvidia_panel source directory

    Returns:
        Tuple of (success, message)
    """
    if not is_admin():
        return False, "Administrator privileges required.\nPlease run GPU-SIM as Administrator."

    install_dir, start_menu, desktop = get_install_paths()

    try:
        # Create installation directory
        install_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created install directory: {install_dir}")

        # Copy all python files and assets
        files_to_copy = [
            "nvidia_control_panel.py",
            "nvidia_style.py",
            "__init__.py",
            "installer.py",
        ]

        panels_dir = install_dir / "panels"
        panels_dir.mkdir(exist_ok=True)

        # Copy main files
        for file_name in files_to_copy:
            src = source_dir / file_name
            if src.exists():
                shutil.copy2(src, install_dir / file_name)

        # Copy panels
        panels_src = source_dir / "panels"
        if panels_src.exists():
            for panel_file in panels_src.glob("*.py"):
                shutil.copy2(panel_file, panels_dir / panel_file.name)

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

        # Copy icon
        icon_src = source_dir.parent / "Agenda" / "512x512.png"
        if icon_src.exists():
            shutil.copy2(icon_src, install_dir / "nvidia_icon.png")

        # Create launcher batch file with proper PYTHONPATH
        launcher_path = install_dir / "NVIDIA Control Panel.bat"
        launcher_content = f'''@echo off
cd /d "{install_dir}"
set PYTHONPATH={install_dir}
pythonw nvidia_control_panel.py
'''
        launcher_path.write_text(launcher_content)

        # Create Start Menu shortcut
        start_menu.mkdir(parents=True, exist_ok=True)
        shortcut_path = start_menu / "NVIDIA Control Panel.lnk"
        create_shortcut(
            target_path=launcher_path,
            shortcut_path=shortcut_path,
            icon_path=install_dir / "nvidia_icon.png",
            description="NVIDIA Control Panel"
        )

        # Create Desktop shortcut
        desktop_shortcut = desktop / "NVIDIA Control Panel.lnk"
        create_shortcut(
            target_path=launcher_path,
            shortcut_path=desktop_shortcut,
            icon_path=install_dir / "nvidia_icon.png",
            description="NVIDIA Control Panel"
        )

        return True, f"NVIDIA Control Panel installed successfully!\n\n" \
                     f"Location: {install_dir}\n\n" \
                     f"Shortcuts created:\n" \
                     f"• Start Menu\n" \
                     f"• Desktop"

    except PermissionError:
        return False, "Permission denied.\nPlease run as Administrator."
    except Exception as e:
        return False, f"Installation failed:\n{str(e)}"


def uninstall_nvidia_control_panel() -> Tuple[bool, str]:
    """
    Uninstall the NVIDIA Control Panel.
    """
    if not is_admin():
        return False, "Administrator privileges required."

    install_dir, start_menu, desktop = get_install_paths()

    try:
        # Remove installation directory
        if install_dir.exists():
            shutil.rmtree(install_dir)

        # Remove Start Menu shortcut
        shortcut_path = start_menu / "NVIDIA Control Panel.lnk"
        if shortcut_path.exists():
            shortcut_path.unlink()

        # Remove Desktop shortcut
        desktop_shortcut = desktop / "NVIDIA Control Panel.lnk"
        if desktop_shortcut.exists():
            desktop_shortcut.unlink()

        return True, "NVIDIA Control Panel uninstalled successfully."

    except Exception as e:
        return False, f"Uninstallation failed:\n{str(e)}"


def is_installed() -> bool:
    """Check if NVIDIA Control Panel is already installed."""
    install_dir, _, _ = get_install_paths()
    return (install_dir / "nvidia_control_panel.py").exists()
