# GPU-SIM: Virtual GPU Simulator for Windows

A Python-based virtual GPU simulator that creates registry entries and UI to simulate GPU presence on Windows systems.

## 🎯 Features

- **Virtual GPU Profiles** - Simulate various NVIDIA/AMD GPUs
- **Registry Configuration** - Create GPU entries visible to Windows
- **Control Panel UI** - NVIDIA Control Panel-style interface
- **WMI Monitoring** - View what applications see for GPU info
- **Backup/Restore** - Safe registry modifications with rollback

## 📁 Project Structure

```
GPU-SIM/
├── config/gpu_profiles/    # GPU configuration JSON files
├── src/
│   ├── core/              # Core configuration management
│   ├── registry/          # Windows registry manipulation
│   ├── wmi/               # WMI query monitoring
│   └── ui/                # PyQt5 control panel UI
├── scripts/               # PowerShell installation scripts
├── driver/                # IDD driver development (future)
├── assets/                # Icons and images
└── docs/                  # Documentation
```

## 🚀 Quick Start

```powershell
# Install dependencies
pip install -r requirements.txt

# Run the control panel
python src/main.py

# Or install as package
pip install -e .
gpu-sim
```

## ⚠️ Requirements

- Windows 10/11
- Python 3.8+
- Administrator privileges (for registry modifications)
- PyQt5

## 📖 Documentation

- [Architecture Guide](docs/ARCHITECTURE.md)
- [Registry Reference](docs/REGISTRY_REFERENCE.md)
- [IDD Driver Roadmap](docs/IDD_ROADMAP.md)

## ⚡ Usage

### 1. Launch Control Panel
```powershell
python src/main.py
```

### 2. Select GPU Profile
Use the dropdown to select a GPU profile (GTX 780 Ti, RTX 3080, etc.)

### 3. Apply Configuration (Admin Required)
```powershell
# Create backup first
.\scripts\backup_restore.ps1 -Backup

# Install virtual GPU
.\scripts\install_gpu.ps1 -Profile nvidia_gtx_780ti
```

### 4. Verify
- Check Task Manager > Performance > GPU
- Run `dxdiag` to see display adapter
- Check Windows Settings > Display

## 🔧 Development

```powershell
# Run tests
python -m pytest tests/ -v

# Run with debug logging
python src/main.py --debug
```

## ⚠️ Disclaimer

This project is for **educational and development purposes only**.
Always test in a virtual machine first and create system restore points before modifying registry.

## 📜 License

MIT License - See LICENSE file
