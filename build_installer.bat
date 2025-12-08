@echo off
REM ============================================================
REM GPU-SIM Build & Installer Generator
REM ============================================================
REM This script compiles the Python applications to executables
REM and then creates the Windows installer using Inno Setup.
REM ============================================================
REM Prerequisites:
REM   - Python 3.8+ with PyInstaller
REM   - Inno Setup 6.x (https://jrsoftware.org/isinfo.php)
REM ============================================================

echo.
echo ========================================
echo   GPU-SIM Build & Installer Generator
echo ========================================
echo.

REM Check if running from project root
if not exist "build\gpu_sim.spec" (
    echo ERROR: Run this script from the GPU-SIM project root directory!
    echo Expected: w:\CodeDeX\GPU-SIM
    exit /b 1
)

REM Create output directories
echo [1/5] Creating build directories...
if not exist "dist" mkdir dist
if not exist "installer\output" mkdir installer\output

REM Build GPU-SIM main application
echo.
echo [2/5] Building GPU-SIM main application...
echo.
pyinstaller --clean build\gpu_sim.spec
if %errorlevel% neq 0 (
    echo ERROR: Failed to build GPU-SIM! Check PyInstaller output.
    exit /b 1
)

REM Build NVIDIA Control Panel
echo.
echo [3/6] Building NVIDIA Control Panel...
echo.
pyinstaller --clean build\nvidia_control_panel.spec
if %errorlevel% neq 0 (
    echo ERROR: Failed to build NVIDIA Control Panel! Check PyInstaller output.
    exit /b 1
)

REM Build GeForce Experience
echo.
echo [4/6] Building GeForce Experience...
echo.
pyinstaller --clean build\geforce_experience.spec
if %errorlevel% neq 0 (
    echo ERROR: Failed to build GeForce Experience! Check PyInstaller output.
    exit /b 1
)

REM Check for Inno Setup
echo.
echo [5/6] Checking for Inno Setup...
set ISCC_PATH=
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    set ISCC_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe
) else if exist "C:\Program Files\Inno Setup 6\ISCC.exe" (
    set ISCC_PATH=C:\Program Files\Inno Setup 6\ISCC.exe
) else (
    echo.
    echo WARNING: Inno Setup not found!
    echo.
    echo The executables have been built successfully in the 'dist' folder.
    echo To create the installer:
    echo   1. Download Inno Setup from https://jrsoftware.org/isdl.php
    echo   2. Install Inno Setup
    echo   3. Open 'installer\gpu_sim_setup.iss' in Inno Setup Compiler
    echo   4. Click Build ^> Compile
    echo.
    echo Alternatively, re-run this script after installing Inno Setup.
    echo.
    goto :done
)

REM Build installer
echo.
echo [6/6] Creating installer package...
echo Using: %ISCC_PATH%
echo.
"%ISCC_PATH%" installer\gpu_sim_setup.iss
if %errorlevel% neq 0 (
    echo ERROR: Installer build failed! Check Inno Setup output.
    exit /b 1
)

:done
echo.
echo ========================================
echo   BUILD COMPLETE!
echo ========================================
echo.
echo Outputs:
echo   - GPU-SIM:          dist\gpu_sim\gpu_sim.exe
echo   - NVIDIA Panel:     dist\nvidia_control_panel\nvidia_control_panel.exe
echo   - GeForce Exp:      dist\geforce_experience\GeForceExperience.exe
if defined ISCC_PATH (
    echo   - Installer:        installer\output\GPU-SIM_Setup_1.0.0.exe
)
echo.
echo Ready for distribution!
echo.
pause
