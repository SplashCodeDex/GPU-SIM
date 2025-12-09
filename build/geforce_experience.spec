# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for GeForce Experience
"""

import sys
from pathlib import Path

project_root = Path(SPECPATH).parent
sys.path.insert(0, str(project_root))

block_cipher = None

a = Analysis(
    ['run_geforce_experience.py'],
    pathex=[str(project_root)],
    binaries=[],
    datas=[
        ('config/gpu_profiles', 'config/gpu_profiles'),
        ('Agenda/512x512.png', 'Agenda'),
    ],
    hiddenimports=[
        'geforce_experience',
        'geforce_experience.gfe_style',
        'geforce_experience.geforce_experience',
        'geforce_experience.tabs',
        'geforce_experience.tabs.home_tab',
        'geforce_experience.tabs.drivers_tab',
        'geforce_experience.tabs.settings_tab',
        'src.core.config_manager',
        'src.core.gpu_profile',
        'PyQt5',
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'json',
        'pathlib',
        'logging',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='GeForceExperience',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='Agenda/512x512.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='geforce_experience',
)
