# GPU-SIM Virtual Display Driver (VDD) Integration

## Overview
This directory contains a fork of [ge9/IddSampleDriver](https://github.com/ge9/IddSampleDriver)
modified for GPU-SIM to display custom GPU names in Windows.

## Key Modification Points

### Driver.cpp - Lines 454-456
```cpp
// MODIFY THESE to change the virtual GPU name
AdapterCaps.EndPointDiagnostics.pEndPointFriendlyName = L"NVIDIA GeForce GTX 780 Ti";
AdapterCaps.EndPointDiagnostics.pEndPointManufacturerName = L"NVIDIA Corporation";
AdapterCaps.EndPointDiagnostics.pEndPointModelName = L"GeForce GTX 780 Ti";
```

### Configuration Files
- `C:\IddSampleDriver\option.txt` - Resolution settings
- `C:\IddSampleDriver\gpu_sim_config.txt` - GPU name (requires driver modification)

## Build Requirements
- Visual Studio 2022
- Windows Driver Kit (WDK)
- Test-signing mode enabled OR valid certificate

## Build Steps
1. Open `IddSampleDriver\IddSampleDriver.sln` in Visual Studio 2022
2. Set target to x64/Release
3. Build solution
4. Copy output to `C:\IddSampleDriver\`
5. Install via Device Manager

## Installation
See the main README.md in this folder.

## Notes
- IMPORTANT: Test in VM first
- Enable test-signing: `bcdedit /set testsigning on`
- Reboot after driver installation
