# GPU-SIM Installer Builder

This directory contains the Inno Setup script for creating a professional Windows installer.

## Prerequisites

1. **Python 3.8+** with PyInstaller installed
2. **Inno Setup 6.x** - Download from [jrsoftware.org](https://jrsoftware.org/isdl.php)

## Building the Installer

### Option 1: Automated Build (Recommended)

Run from the project root:
```batch
build_installer.bat
```

This will:
1. Compile GPU-SIM to `dist\gpu_sim\`
2. Compile NVIDIA Control Panel to `dist\nvidia_control_panel\`
3. Generate the installer to `installer\output\GPU-SIM_Setup_1.0.0.exe`

### Option 2: Manual Build

1. **Build the executables:**
   ```batch
   pyinstaller --clean build\gpu_sim.spec
   pyinstaller --clean build\nvidia_control_panel.spec
   ```

2. **Compile the installer:**
   - Open `installer\gpu_sim_setup.iss` in Inno Setup Compiler
   - Click **Build** → **Compile**
   - Find the output in `installer\output\`

## Installer Features

- ✅ **Component Selection** - Install GPU-SIM, NVIDIA Panel, or both
- ✅ **Desktop Shortcuts** - Optional desktop icons
- ✅ **Context Menu** - Optional Windows right-click integration
- ✅ **Auto-Start** - Optional startup with Windows
- ✅ **Uninstaller** - Clean removal with registry cleanup
- ✅ **Modern UI** - Professional wizard-style interface

## Output

After building, you'll find:
- `installer\output\GPU-SIM_Setup_1.0.0.exe` - The installer (~50-100MB)

## Testing

Always test the installer in a **Virtual Machine** before distribution:
1. Take a VM snapshot
2. Run the installer
3. Test GPU-SIM and NVIDIA Control Panel
4. Test the uninstaller
5. Verify all registry entries are cleaned up
