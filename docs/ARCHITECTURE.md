# GPU-SIM Architecture

This document describes the architecture of the GPU-SIM virtual GPU simulator.

## Project Structure

```
GPU-SIM/
├── config/
│   └── gpu_profiles/           # JSON GPU profile definitions
├── src/
│   ├── core/                   # Core business logic
│   │   ├── config_manager.py   # Profile loading/saving
│   │   └── gpu_profile.py      # Profile data class
│   ├── registry/               # Windows registry operations
│   │   ├── backup_manager.py   # Backup/restore functionality
│   │   └── gpu_registry.py     # Registry read/write
│   ├── wmi/                    # WMI system queries
│   │   └── wmi_monitor.py      # GPU info from WMI
│   └── ui/                     # PyQt5 user interface
│       ├── main_window.py      # Main application window
│       ├── panels/             # Content panels
│       └── widgets/            # Reusable widgets
├── scripts/                    # PowerShell automation
│   ├── backup_restore.ps1      # Registry backup
│   ├── install_gpu.ps1         # Profile installation
│   └── uninstall_gpu.ps1       # Profile removal
└── docs/                       # Documentation
```

## Component Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                        │
│  ┌───────────────┐  ┌───────────────┐  ┌──────────────┐│
│  │  Home Panel   │  │ GPU Info Panel│  │ 3D Settings  ││
│  └───────────────┘  └───────────────┘  └──────────────┘│
│  ┌─────────────────────────────────────────────────────┐│
│  │               GPU Selector Widget                   ││
│  └─────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    Core Layer                            │
│  ┌───────────────────┐  ┌──────────────────────────────┐│
│  │  ConfigManager    │  │      GPUProfile             ││
│  │  - load_profiles  │  │  - name, vram, clocks       ││
│  │  - save_profile   │  │  - registry_entries         ││
│  │  - get_profile    │  │  - to_dict / from_dict      ││
│  └───────────────────┘  └──────────────────────────────┘│
└─────────────────────────────────────────────────────────┘
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ Registry Module │ │   WMI Module    │ │ PowerShell      │
│ - read adapters │ │ - query WMI     │ │ - backup/restore│
│ - apply profile │ │ - monitor GPUs  │ │ - install/remove│
│ - backup/restore│ │ - display info  │ │                 │
└─────────────────┘ └─────────────────┘ └─────────────────┘
          │                │
          ▼                ▼
┌─────────────────────────────────────────────────────────┐
│                 Windows System                           │
│  ┌───────────────┐  ┌──────────────┐  ┌───────────────┐│
│  │   Registry    │  │     WMI      │  │ Task Manager  ││
│  │   HKLM\...    │  │ Win32_Video  │  │    DxDiag     ││
│  └───────────────┘  └──────────────┘  └───────────────┘│
└─────────────────────────────────────────────────────────┘
```

## Data Flow

1. **Profile Loading**: `ConfigManager` loads JSON profiles from `config/gpu_profiles/`
2. **Profile Selection**: User selects profile via `GPUSelector` widget
3. **UI Update**: All panels receive profile and update display
4. **Apply Profile**: `GPURegistry` writes entries to Windows registry
5. **Verification**: `WMIMonitor` queries system to verify changes

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| PyQt5 for UI | Cross-platform compatible, rich widgets, NVIDIA Control Panel aesthetic |
| JSON profiles | Human-readable, easy to edit, version control friendly |
| Registry backup | Safety first - all modifications can be reverted |
| Modular panels | Easy to add/remove features without breaking others |
| Singleton managers | Single source of truth for config and registry state |

## Limitations

- **Registry-only**: Modifications are cosmetic; actual GPU functionality not emulated
- **Admin required**: Registry writes need elevated privileges
- **Restart needed**: Some changes only take effect after reboot
- **No driver**: Full GPU emulation requires IDD driver (see IDD_ROADMAP.md)
