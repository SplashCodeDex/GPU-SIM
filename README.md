# GPU-SIM: Virtual GPU Simulator for Windows

[![GitHub release](https://img.shields.io/github/v/release/SplashCodeDex/GPU-SIM?style=flat-square)](https://github.com/SplashCodeDex/GPU-SIM/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Windows](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

A powerful Python-based virtual GPU simulator that creates realistic GPU presence on Windows systems, complete with a fake NVIDIA Control Panel and live metrics dashboard.

## 🎮 What It Does

GPU-SIM simulates a GPU so convincingly that:
- **Task Manager** shows your fake GPU under Performance
- **DxDiag** displays the spoofed GPU adapter
- **Windows Settings** recognizes the virtual GPU
- **NVIDIA Control Panel** shows matching specifications

## ✨ Features

### Core Simulation
- 🖥️ **9 GPU Profiles** - RTX 4090, 4080, 4070 Ti, 3090, 3080, RX 7900 XTX, RX 6800 XT, Arc A770, GTX 780 Ti
- 📝 **Registry Spoofing** - Modify Windows registry to simulate GPU presence
- 🔒 **Backup/Restore** - Safe registry modifications with rollback

### NVIDIA Control Panel (NEW!)
- 🟢 **Authentic Replica** - Looks identical to the real NVIDIA Control Panel
- 📊 **System Information** - Shows GPU name, VRAM, drivers, CUDA cores
- ⚙️ **3D Settings** - Antialiasing, texture filtering, VSync options
- 🖵 **Display Settings** - Resolution and refresh rate selection
- 🌙 **Dark/Light Theme** - Toggle via View menu

### Live Metrics Dashboard
- 📈 **Animated Gauges** - GPU/Memory utilization with smooth animations
- 🌡️ **Temperature** - Fake temps with realistic idle/load curves
- ⚡ **Power Draw** - Simulated wattage based on load
- 🔢 **Clock Speeds** - Dynamic GPU/Memory clocks

### Additional Features
- 📌 **System Tray** - Quick profile switching, minimize to tray
- ✏️ **Profile Editor** - Customize VRAM with quick GB buttons
- 🔌 **VDD Support** - Virtual Display Driver integration
- 🛡️ **GPU-Z Bypass** - Fake adapter info generation

## 📁 Project Structure

```
GPU-SIM/
├── src/                    # Main application
│   ├── core/               # Config, profiles, GPU dataclasses
│   ├── registry/           # Windows registry manipulation
│   ├── wmi/                # WMI GPU monitoring
│   ├── vdd/                # Virtual Display Driver
│   ├── metrics/            # Fake metrics generator
│   ├── hooks/              # GPU-Z bypass hooks
│   └── ui/                 # PyQt5 control panel UI
├── nvidia_panel/           # NVIDIA Control Panel replica
│   ├── panels/             # System Info, 3D Settings, Display
│   └── installer.py        # Install to Program Files
├── config/gpu_profiles/    # JSON GPU configurations
├── build/                  # PyInstaller specs
├── tests/                  # Unit tests
└── docs/                   # Documentation
```

## 🚀 Quick Start

### Option 1: Download Release
Download `GPU-SIM.exe` from [Releases](https://github.com/SplashCodeDex/GPU-SIM/releases)

### Option 2: Run from Source
```powershell
# Clone
git clone https://github.com/SplashCodeDex/GPU-SIM.git
cd GPU-SIM

# Install dependencies
pip install -r requirements.txt

# Run
python src/main.py
```

### Option 3: Build Executable
```powershell
pip install pyinstaller
pyinstaller build/gpu_sim.spec --clean
# Output: dist/GPU-SIM.exe
```

## ⚠️ Requirements

- **Windows 10/11**
- **Python 3.8+**
- **Administrator privileges** (for registry modifications)
- **PyQt5, pywin32, WMI**

## 📖 Usage

1. **Launch GPU-SIM** - Run `GPU-SIM.exe` or `python src/main.py`
2. **Select GPU Profile** - Use dropdown to pick a GPU (RTX 4090, etc.)
3. **Install NVIDIA Control Panel** - Click the green button on Home
4. **Apply to System** - Click "Apply to System" (requires Admin)
5. **Restart** - Reboot for changes to take effect

### Verification
- Check **Task Manager > Performance > GPU**
- Run `dxdiag` and check Display tab
- Open **NVIDIA Control Panel** from Start Menu

## 🔧 Development

```powershell
# Run tests
python -m pytest tests/ -v

# Run with debug
python src/main.py --debug

# Check imports
python -c "from src.ui.main_window import MainWindow; print('OK')"
```

## ⚠️ Disclaimer

This project is for **educational and development purposes only**.
- Always test in a virtual machine first
- Create a system restore point before modifying registry
- Not for use in any deceptive or malicious activities

## 📜 License

MIT License - See [LICENSE](LICENSE) file

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📋 Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.
