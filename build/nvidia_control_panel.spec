# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller Spec File for NVIDIA Control Panel
Builds a standalone .exe that looks and works like the real NVIDIA Control Panel.

Run: pyinstaller build/nvidia_control_panel.spec --clean
"""

from pathlib import Path

project_root = Path(SPECPATH).parent

a = Analysis(
    [str(project_root / 'run_nvidia_panel.py')],
    pathex=[str(project_root)],
    binaries=[],
    datas=[
        # GPU profiles
        (str(project_root / 'config' / 'gpu_profiles'), 'config/gpu_profiles'),
        # NVIDIA icon
        (str(project_root / 'Agenda' / '512x512.png'), 'Agenda'),
        # src/core (required for profiles)
        (str(project_root / 'src' / 'core'), 'src/core'),
    ],
    hiddenimports=[
        'PyQt5',
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'nvidia_panel',
        'nvidia_panel.nvidia_control_panel',
        'nvidia_panel.nvidia_style',
        'nvidia_panel.nvidia_tray',
        'nvidia_panel.panels',
        'nvidia_panel.panels.system_info',
        'nvidia_panel.panels.manage_3d',
        'nvidia_panel.panels.display_settings',
        'src.core.config_manager',
        'src.core.gpu_profile',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib', 'numpy', 'scipy', 'pandas'],
    noarchive=False,
)

pyz = PYZ(a.pure)

# Single-file executable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='NVIDIA Control Panel',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(project_root / 'Agenda' / '512x512.ico') if (project_root / 'Agenda' / '512x512.ico').exists() else None,
    version=None,  # Could add version info later
)
