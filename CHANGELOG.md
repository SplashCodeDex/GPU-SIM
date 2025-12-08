# Changelog

All notable changes to GPU-SIM will be documented in this file.

## [1.1.0] - 2024-12-08

### Added
- **PhysX Configuration Panel**: Simulated PhysX processor selection and visual indicator settings
- **Surround Configuration Panel**: Multi-monitor preview with NVIDIA Surround simulation
- **GeForce Experience App**: Full replica with Home, Drivers, and Settings tabs
  - Game library simulation with optimization status
  - Driver history and update simulation
  - ShadowPlay and overlay settings
  - System tray integration
- **Professional Installer**: Inno Setup-based installer with component selection
  - Full/custom installation options
  - Desktop shortcuts and context menu integration
  - Windows autostart configuration
  - Clean uninstaller with registry cleanup

### Changed
- Updated installer to include all 3 applications (GPU-SIM, Control Panel, GeForce Experience)
- Build script now compiles all executables in sequence

## [1.0.0] - 2024-12-08

### Added
- **9 GPU Profiles**: RTX 4090, 4080, 4070 Ti, 3090, 3080, RX 7900 XTX, RX 6800 XT, Intel Arc A770, GTX 780 Ti
- **NVIDIA Control Panel Replica**: Standalone app with System Info, 3D Settings, Display panels
- **Live Metrics Dashboard**: Animated GPU gauges (utilization, temp, power, clocks)
- **Profile Editor**: Customize VRAM and other specs with quick GB buttons
- **System Tray Integration**: Quick profile switching, minimize to tray
- **Virtual Display Driver Support**: VDD detection and installation guide
- **GPU-Z Detection Bypass**: Fake adapter info and DxDiag XML generation
- **Registry Spoofing**: Apply GPU profiles to Windows registry
- **WMI Monitoring**: View real GPU info as seen by Windows
- **PyInstaller Packaging**: Build standalone GPU-SIM.exe
- **GitHub Actions**: Automated release builds on tag push

### Technical
- Modular architecture with 8 src modules
- PyQt5-based modern UI with dark theme
- JSON-based GPU profile configuration
- Background metrics generation thread
- Win32 API integration for shortcuts

## [0.1.0] - 2024-12-01

### Added
- Initial prototype with single-file UI
- Basic registry modification concept
