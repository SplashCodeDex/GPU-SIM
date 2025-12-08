# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller Spec File for GPU-SIM
Run: pyinstaller build/gpu_sim.spec
"""

import sys
from pathlib import Path

# Add project paths
project_root = Path(SPECPATH).parent
src_path = project_root / 'src'

a = Analysis(
    [str(project_root / 'src' / 'main.py')],
    pathex=[str(project_root), str(src_path)],
    binaries=[],
    datas=[
        # Include GPU profiles
        (str(project_root / 'config' / 'gpu_profiles'), 'config/gpu_profiles'),
        # Include assets
        (str(project_root / 'assets'), 'assets'),
        # Include docs
        (str(project_root / 'docs'), 'docs'),
        # Include scripts (optional, for advanced users)
        (str(project_root / 'scripts'), 'scripts'),
    ],
    hiddenimports=[
        'PyQt5',
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'win32api',
        'win32con',
        'winreg',
        'wmi',
        'pythoncom',
        'pywintypes',
        'json',
        'yaml',
        'jsonschema',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'numpy',
        'scipy',
        'pandas',
    ],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='GPU-SIM',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window (GUI app)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(project_root / 'assets' / 'icons' / 'gpu_sim.ico') if (project_root / 'assets' / 'icons' / 'gpu_sim.ico').exists() else None,
    version_info=None,
)

# Also create a directory-based build for debugging
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='GPU-SIM',
)
