# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller Spec File for NVIDIA Control Panel
Run: pyinstaller build/nvidia_panel.spec
"""

from pathlib import Path

project_root = Path(SPECPATH).parent

a = Analysis(
    [str(project_root / 'run_nvidia_panel.py')],
    pathex=[str(project_root)],
    binaries=[],
    datas=[
        (str(project_root / 'config' / 'gpu_profiles'), 'config/gpu_profiles'),
        (str(project_root / 'Agenda' / '512x512.png'), 'Agenda'),
    ],
    hiddenimports=[
        'PyQt5',
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib', 'numpy'],
    noarchive=False,
)

pyz = PYZ(a.pure)

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
    console=False,
    icon=str(project_root / 'Agenda' / '512x512.png') if (project_root / 'Agenda' / '512x512.png').exists() else None,
)
