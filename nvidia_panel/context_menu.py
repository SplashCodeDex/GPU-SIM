"""
NVIDIA Context Menu Integration
Adds "NVIDIA Control Panel" to the desktop and folder right-click context menu.
"""

import os
import sys
import winreg
import ctypes
import logging
from pathlib import Path
from typing import Tuple

logger = logging.getLogger(__name__)


def is_admin() -> bool:
    """Check if running as administrator."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def get_nvidia_panel_path() -> Path:
    """Get the path to NVIDIA Control Panel executable."""
    # Check common installation locations
    paths = [
        Path(os.environ.get("PROGRAMFILES", "")) / "NVIDIA Corporation" / "Control Panel" / "NVIDIA Control Panel.bat",
        Path(__file__).parent.parent / "dist" / "NVIDIA Control Panel.exe",
        Path(__file__).parent / "nvidia_control_panel.py",
    ]

    for path in paths:
        if path.exists():
            return path

    return paths[0]  # Return expected path even if doesn't exist


def add_context_menu() -> Tuple[bool, str]:
    """
    Add "NVIDIA Control Panel" to the right-click context menu.

    Adds to:
    - Desktop right-click
    - Folder background right-click

    Returns:
        Tuple of (success, message)
    """
    if not is_admin():
        return False, "Administrator privileges required."

    nvidia_path = get_nvidia_panel_path()

    try:
        # Add to Desktop context menu
        key_path = r"Directory\Background\shell\NVIDIAControlPanel"

        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key_path) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "NVIDIA Control Panel")
            winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, str(nvidia_path))

        # Add command
        cmd_path = key_path + r"\command"
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, cmd_path) as key:
            if nvidia_path.suffix == ".py":
                command = f'pythonw "{nvidia_path}"'
            else:
                command = f'"{nvidia_path}"'
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, command)

        logger.info("Added NVIDIA Control Panel to context menu")
        return True, "NVIDIA Control Panel added to right-click menu!\n\nRight-click on desktop to see it."

    except PermissionError:
        return False, "Permission denied. Run as Administrator."
    except Exception as e:
        return False, f"Failed to add context menu:\n{str(e)}"


def remove_context_menu() -> Tuple[bool, str]:
    """
    Remove "NVIDIA Control Panel" from the right-click context menu.

    Returns:
        Tuple of (success, message)
    """
    if not is_admin():
        return False, "Administrator privileges required."

    try:
        key_path = r"Directory\Background\shell\NVIDIAControlPanel"

        # Delete command key first
        try:
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, key_path + r"\command")
        except FileNotFoundError:
            pass

        # Delete main key
        try:
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, key_path)
        except FileNotFoundError:
            pass

        logger.info("Removed NVIDIA Control Panel from context menu")
        return True, "NVIDIA Control Panel removed from right-click menu."

    except Exception as e:
        return False, f"Failed to remove context menu:\n{str(e)}"


def is_context_menu_installed() -> bool:
    """Check if context menu entry exists."""
    try:
        key_path = r"Directory\Background\shell\NVIDIAControlPanel"
        winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, key_path)
        return True
    except FileNotFoundError:
        return False


def add_autostart() -> Tuple[bool, str]:
    """
    Add NVIDIA Control Panel to Windows startup.

    Returns:
        Tuple of (success, message)
    """
    nvidia_path = get_nvidia_panel_path()

    try:
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
            if nvidia_path.suffix == ".py":
                command = f'pythonw "{nvidia_path}"'
            else:
                command = f'"{nvidia_path}"'
            winreg.SetValueEx(key, "NVIDIAControlPanel", 0, winreg.REG_SZ, command)

        logger.info("Added NVIDIA Control Panel to startup")
        return True, "NVIDIA Control Panel will start with Windows.\n\nIt will appear in the system tray on login."

    except Exception as e:
        return False, f"Failed to add to startup:\n{str(e)}"


def remove_autostart() -> Tuple[bool, str]:
    """
    Remove NVIDIA Control Panel from Windows startup.

    Returns:
        Tuple of (success, message)
    """
    try:
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.DeleteValue(key, "NVIDIAControlPanel")

        logger.info("Removed NVIDIA Control Panel from startup")
        return True, "NVIDIA Control Panel removed from startup."

    except FileNotFoundError:
        return True, "NVIDIA Control Panel was not in startup."
    except Exception as e:
        return False, f"Failed to remove from startup:\n{str(e)}"


def is_autostart_enabled() -> bool:
    """Check if autostart is enabled."""
    try:
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            winreg.QueryValueEx(key, "NVIDIAControlPanel")
            return True
    except (FileNotFoundError, OSError):
        return False
