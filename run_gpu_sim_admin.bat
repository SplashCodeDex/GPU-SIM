@echo off
:: GPU-SIM Admin Launcher
:: This script requests UAC elevation and runs GPU-SIM as Administrator

:: Check for admin rights
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running GPU-SIM as Administrator...
    cd /d "%~dp0"
    python src/main.py
) else (
    echo Requesting Administrator privileges...
    powershell -Command "Start-Process cmd -ArgumentList '/c cd /d %~dp0 && python src/main.py' -Verb RunAs"
)
