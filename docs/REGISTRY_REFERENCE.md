# Windows Registry Reference for GPU/Display

This document details the Windows registry paths used for GPU and display adapter configuration.

## Primary Registry Paths

### 1. Display Adapter Class

```
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}
```

This is the **Display Adapter device class**. Each installed GPU has a numbered subkey (0000, 0001, etc.).

**Key Values:**

| Value Name | Type | Description |
|------------|------|-------------|
| `DriverDesc` | REG_SZ | GPU name shown in Device Manager |
| `ProviderName` | REG_SZ | Driver provider (NVIDIA, AMD, Intel) |
| `DriverVersion` | REG_SZ | Driver version string |
| `DriverDate` | REG_SZ | Driver date |
| `HardwareInformation.AdapterString` | REG_SZ | Adapter name |
| `HardwareInformation.BiosString` | REG_SZ | BIOS version |
| `HardwareInformation.ChipType` | REG_SZ | GPU chip type |
| `HardwareInformation.DACType` | REG_SZ | DAC type |
| `HardwareInformation.MemorySize` | REG_DWORD | VRAM in bytes |

### 2. Video Controllers

```
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Video
```

Contains GUID subkeys for each video controller. Each GUID has numbered subkeys (0000, etc.) for display outputs.

**Key Values:**

| Value Name | Type | Description |
|------------|------|-------------|
| `Device Description` | REG_SZ | Monitor/display description |
| `DefaultSettings.XResolution` | REG_DWORD | Default horizontal resolution |
| `DefaultSettings.YResolution` | REG_DWORD | Default vertical resolution |
| `DefaultSettings.VRefresh` | REG_DWORD | Refresh rate |
| `Attach.ToDesktop` | REG_DWORD | Whether attached to desktop |

### 3. Graphics Drivers

```
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\GraphicsDrivers
```

**Subkeys:**

| Subkey | Purpose |
|--------|---------|
| `Configuration` | Display configuration for monitor setups |
| `Connectivity` | Display connectivity information |
| `ScaleFactors` | Display scaling settings |

### 4. WMI Provider Path

WMI's `Win32_VideoController` reads from:
- Display adapter class entries
- DirectX diagnostic information
- Hardware inventory

## Registry Entry Examples

### NVIDIA GPU Example

```reg
[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}\0000]
"DriverDesc"="NVIDIA GeForce RTX 3080"
"ProviderName"="NVIDIA"
"DriverVersion"="31.0.15.4633"
"HardwareInformation.AdapterString"="NVIDIA GeForce RTX 3080"
"HardwareInformation.BiosString"="Version 94.02.42.00.0F"
"HardwareInformation.ChipType"="GeForce RTX 3080"
"HardwareInformation.DACType"="Integrated RAMDAC"
"HardwareInformation.MemorySize"=dword:280000000
```

### AMD GPU Example

```reg
[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}\0000]
"DriverDesc"="AMD Radeon RX 6800 XT"
"ProviderName"="Advanced Micro Devices, Inc."
"DriverVersion"="31.0.21003.1002"
"HardwareInformation.AdapterString"="AMD Radeon RX 6800 XT"
"HardwareInformation.ChipType"="AMD Radeon Graphics"
"HardwareInformation.DACType"="Internal DAC(400MHz)"
"HardwareInformation.MemorySize"=dword:400000000
```

## Backup Commands

### Export All GPU Registry

```powershell
reg export "HKLM\SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}" gpu_class.reg
reg export "HKLM\SYSTEM\CurrentControlSet\Control\Video" gpu_video.reg
reg export "HKLM\SYSTEM\CurrentControlSet\Control\GraphicsDrivers" gpu_drivers.reg
```

### Restore

```powershell
reg import gpu_class.reg
reg import gpu_video.reg
reg import gpu_drivers.reg
```

## Important Notes

> ⚠️ **Warning**: Incorrect registry modifications can cause system instability or prevent Windows from booting.

> 💡 **Tip**: Always create a System Restore Point before modifying registry.

> 📝 **Note**: Some changes require a system restart to take effect.

> 🔒 **Security**: Admin privileges required for HKLM modifications.
