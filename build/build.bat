@echo off
REM GPU-SIM Build Script
REM Creates a standalone .exe using PyInstaller

echo ======================================
echo   GPU-SIM Build Script
echo ======================================
echo.

REM Check for PyInstaller
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    python -m pip install pyinstaller
)

echo.
echo Building GPU-SIM.exe...
echo.

cd /d "%~dp0.."
python -m PyInstaller build/gpu_sim.spec --clean --noconfirm

echo.
if exist "dist\GPU-SIM\GPU-SIM.exe" (
    echo ======================================
    echo   BUILD SUCCESSFUL!
    echo ======================================
    echo.
    echo Output: dist\GPU-SIM\GPU-SIM.exe
    echo.
    echo To run: dist\GPU-SIM\GPU-SIM.exe
) else if exist "dist\GPU-SIM.exe" (
    echo ======================================
    echo   BUILD SUCCESSFUL!
    echo ======================================
    echo.
    echo Output: dist\GPU-SIM.exe
) else (
    echo ======================================
    echo   BUILD FAILED
    echo ======================================
    echo Check the output above for errors.
)

pause
