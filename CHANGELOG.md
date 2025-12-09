# Changelog

All notable changes to GPU-SIM will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v1.2.0] - 2024-12-09

### Added
- **GPU-Z Bypass Toggle** - Checkbox in home panel to enable/disable GPU-Z spoofing
- **meson & ninja** added to requirements.txt for building v2.0.0 features
- Updated project structure documentation in README

### Changed
- README.md updated with v1.2.0 features and new project structure

### v2.0.0 Preview (Code Ready, Build Required)
- VDD (Virtual Display Driver) for Task Manager GPU spoofing
- fakenvapi DLL for GPU-Z/HWiNFO bypass

---

## [v1.1.0] - 2024-12-08

### Added
- **One-Click Installer Wizard** - 5-step wizard for easy GPU-SIM setup
- **Verification Panel** - Checklist to verify spoofing worked (DxDiag, Task Manager, etc.)
- **GeForce Experience** - Full replica application with:
  - Games tab (8 fake games with optimization status)
  - Drivers tab (fake driver versions and update simulation)
  - Settings tab (general, optimization, overlay, account settings)
- **Auto-Admin Elevation** - GPU-SIM now requests admin privileges on startup
- **GFE Installer** - Install GeForce Experience from NVIDIA Control Panel

### Changed
- Simplified GPU-SIM UI - Removed redundant panels (Display, 3D Settings, Live Metrics, VDD)
- Kept essential panels: Home, GPU Information, Profile Editor, Verification
- Dynamic admin status footer in home panel

### Fixed
- GitHub Actions workflow - Fixed .spec file tracking in .gitignore
- Build artifact cleanup - Removed accidentally tracked PyInstaller files

---

## [v1.0.0] - 2024-12-01

### Added
- **GPU-SIM Core Application**
  - 9 GPU profiles (RTX 4090, 4080, 4070 Ti, 3090, 3080, RX 7900 XTX, RX 6800 XT, Arc A770, GTX 780 Ti)
  - Registry spoofing for Windows GPU detection
  - WMI data spoofing
  - Backup/Restore functionality

- **NVIDIA Control Panel Replica**
  - System Information panel
  - 3D Settings panel
  - Display Settings panel
  - Surround panel
  - PhysX panel
  - Dark/Light theme toggle

- **Live Metrics Dashboard**
  - Animated GPU utilization gauges
  - Temperature monitoring (simulated)
  - Power draw display
  - Clock speed monitoring

- **Additional Features**
  - System tray integration
  - Profile editor with custom VRAM
  - PyInstaller build support
  - Inno Setup installer

---

## [Unreleased]

### Planned for v2.0.0
- [ ] Virtual Display Driver (VDD) for Task Manager GPU tab
- [ ] GPU-Z/HWiNFO bypass via fakenvapi DLL
- [ ] More GPU profiles (RTX 4060, 3060, GTX 1080 Ti)
- [ ] Enhanced verification with screenshots

---

[v1.2.0]: https://github.com/SplashCodeDex/GPU-SIM/releases/tag/v1.2.0
[v1.1.0]: https://github.com/SplashCodeDex/GPU-SIM/releases/tag/v1.1.0
[v1.0.0]: https://github.com/SplashCodeDex/GPU-SIM/releases/tag/v1.0.0
