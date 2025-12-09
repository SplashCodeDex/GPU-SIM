# GPU-SIM Virtual Display Driver (VDD) Integration

## Overview
This directory contains the Virtual Display Driver for GPU-SIM, using
[VirtualDrivers/Virtual-Display-Driver](https://github.com/VirtualDrivers/Virtual-Display-Driver) (MttVDD).

The VDD creates a virtual display adapter that appears in Task Manager's Performance tab with your spoofed GPU name.

## Driver Location

| Component | Path |
|-----------|------|
| **Source** | `Virtual-Display-Driver/Virtual Display Driver (HDR)/MttVDD/` |
| **Build Output** | `Virtual-Display-Driver/Virtual Display Driver (HDR)/x64/Release/MttVDD/` |
| **Installer Script** | `../../src/vdd/vdd_installer.py` |

## Key Modifications Made

### Driver.cpp - Lines 166-174
```cpp
// GPU-SIM: Modified defaults for NVIDIA GeForce GTX 780 Ti spoofing
bool monitorEmulationEnabled = true;
bool manufacturerEmulationEnabled = true;
wstring manufacturerName = L"NVIDIA Corporation";
wstring modelName = L"NVIDIA GeForce GTX 780 Ti";
wstring serialNumber = L"GPU-SIM-780Ti";
```

### MttVDD.vcxproj
- Disabled Spectre mitigation for all x64/ARM64 configurations
- `<Driver_SpectreMitigation>false</Driver_SpectreMitigation>`

## Build Requirements
- Visual Studio 2022 with C++ Desktop Development
- Windows Driver Kit (WDK) 10.0.26100+
- Test-signing mode enabled

## Build Steps
```powershell
# 1. Open solution in Visual Studio 2022
#    Virtual-Display-Driver/Virtual Display Driver (HDR)/MttVDD.sln

# 2. Set configuration: Release | x64

# 3. Build (Ctrl+Shift+B)
#    Output: x64/Release/MttVDD/
```

## Installation

### Step 1: Enable Test-Signing (requires Admin + reboot)
```powershell
bcdedit /set testsigning on
# Reboot your computer
```

### Step 2: Install Driver
```powershell
# Using the VDD installer script
python src/vdd/vdd_installer.py install

# Or manually via Device Manager:
# 1. Open Device Manager
# 2. Action → Add Legacy Hardware
# 3. Select "Display adapters"
# 4. Click "Have Disk..." and browse to MttVDD.inf
```

## Configuration Files

| File | Location | Purpose |
|------|----------|---------|
| `option.txt` | `C:\VirtualDisplayDriver\` | Virtual display resolution settings |
| `vdd_settings.xml` | `C:\VirtualDisplayDriver\` | Advanced VDD configuration |

## Notes

> [!WARNING]
> **Always test in a VM first!**

- Test-signing shows a watermark on desktop (normal)
- Uninstall: `python src/vdd/vdd_installer.py uninstall`
- Check status: `python src/vdd/vdd_installer.py status`

## Credits

- Based on [VirtualDrivers/Virtual-Display-Driver](https://github.com/VirtualDrivers/Virtual-Display-Driver)
- Original [ge9/IddSampleDriver](https://github.com/ge9/IddSampleDriver)
- Microsoft IddCx sample driver
