<#
.SYNOPSIS
    Backup and restore GPU-related registry entries.

.DESCRIPTION
    This script creates backups of GPU-related registry keys and can restore them.
    Always run this before making any registry modifications.

.PARAMETER Backup
    Create a new backup of GPU registry entries.

.PARAMETER Restore
    Restore from a backup file.

.PARAMETER BackupFile
    Path to specific backup file for restore operation.

.PARAMETER List
    List available backup files.

.EXAMPLE
    .\backup_restore.ps1 -Backup
    Creates a new backup with timestamp.

.EXAMPLE
    .\backup_restore.ps1 -Restore -BackupFile "backups\gpu_backup_20231215.reg"
    Restores from specified backup.

.EXAMPLE
    .\backup_restore.ps1 -List
    Lists all available backups.

.NOTES
    Requires Administrator privileges.
    Author: GPU-SIM Project
#>

param(
    [switch]$Backup,
    [switch]$Restore,
    [switch]$List,
    [string]$BackupFile = ""
)

# Configuration
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$BackupDir = Join-Path $ProjectRoot "backups"

# Registry paths to backup
$RegistryPaths = @(
    "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Video",
    "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}",
    "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\GraphicsDrivers"
)

# Ensure backup directory exists
if (-not (Test-Path $BackupDir)) {
    New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null
    Write-Host "[INFO] Created backup directory: $BackupDir" -ForegroundColor Green
}

function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Create-Backup {
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "  GPU Registry Backup" -ForegroundColor Cyan
    Write-Host "========================================`n" -ForegroundColor Cyan

    if (-not (Test-Administrator)) {
        Write-Host "[ERROR] This script requires Administrator privileges!" -ForegroundColor Red
        Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
        return
    }

    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $backupCount = 0

    foreach ($path in $RegistryPaths) {
        $safeName = $path -replace "\\", "_" -replace "{", "" -replace "}", "" -replace "HKEY_LOCAL_MACHINE_", ""
        $safeName = $safeName.Substring(0, [Math]::Min(50, $safeName.Length))
        $backupFile = Join-Path $BackupDir "${safeName}_${timestamp}.reg"

        Write-Host "[*] Backing up: $path" -ForegroundColor Yellow

        try {
            $result = reg export $path $backupFile /y 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Host "    [OK] Saved to: $backupFile" -ForegroundColor Green
                $backupCount++
            } else {
                Write-Host "    [WARN] Could not backup (may not exist): $path" -ForegroundColor DarkYellow
            }
        } catch {
            Write-Host "    [ERROR] Failed: $_" -ForegroundColor Red
        }
    }

    Write-Host "`n[SUCCESS] Created $backupCount backup(s) in: $BackupDir" -ForegroundColor Green
}

function Restore-Backup {
    param([string]$File)

    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "  GPU Registry Restore" -ForegroundColor Cyan
    Write-Host "========================================`n" -ForegroundColor Cyan

    if (-not (Test-Administrator)) {
        Write-Host "[ERROR] This script requires Administrator privileges!" -ForegroundColor Red
        return
    }

    if (-not $File) {
        Write-Host "[ERROR] Please specify a backup file with -BackupFile parameter" -ForegroundColor Red
        Write-Host "Use -List to see available backups" -ForegroundColor Yellow
        return
    }

    # Handle relative paths
    if (-not [System.IO.Path]::IsPathRooted($File)) {
        $File = Join-Path $ProjectRoot $File
    }

    if (-not (Test-Path $File)) {
        Write-Host "[ERROR] Backup file not found: $File" -ForegroundColor Red
        return
    }

    Write-Host "[*] Restoring from: $File" -ForegroundColor Yellow
    Write-Host "[!] WARNING: This will modify your system registry!" -ForegroundColor Red

    $confirmation = Read-Host "Are you sure you want to continue? (yes/no)"
    if ($confirmation -ne "yes") {
        Write-Host "[CANCELLED] Restore operation cancelled" -ForegroundColor Yellow
        return
    }

    try {
        reg import $File
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[SUCCESS] Registry restored successfully!" -ForegroundColor Green
            Write-Host "[INFO] You may need to restart your computer for changes to take effect" -ForegroundColor Cyan
        } else {
            Write-Host "[ERROR] Failed to restore registry" -ForegroundColor Red
        }
    } catch {
        Write-Host "[ERROR] Failed: $_" -ForegroundColor Red
    }
}

function List-Backups {
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "  Available GPU Backups" -ForegroundColor Cyan
    Write-Host "========================================`n" -ForegroundColor Cyan

    $backups = Get-ChildItem -Path $BackupDir -Filter "*.reg" -ErrorAction SilentlyContinue |
               Sort-Object LastWriteTime -Descending

    if ($backups.Count -eq 0) {
        Write-Host "[INFO] No backup files found in: $BackupDir" -ForegroundColor Yellow
        Write-Host "Run with -Backup to create a backup" -ForegroundColor Cyan
        return
    }

    Write-Host "Found $($backups.Count) backup(s):`n" -ForegroundColor Green

    $i = 1
    foreach ($backup in $backups) {
        $size = "{0:N2} KB" -f ($backup.Length / 1KB)
        $date = $backup.LastWriteTime.ToString("yyyy-MM-dd HH:mm:ss")
        Write-Host "  [$i] $($backup.Name)" -ForegroundColor White
        Write-Host "      Date: $date | Size: $size" -ForegroundColor Gray
        Write-Host "      Path: $($backup.FullName)" -ForegroundColor DarkGray
        Write-Host ""
        $i++
    }
}

# Main execution
if ($Backup) {
    Create-Backup
} elseif ($Restore) {
    Restore-Backup -File $BackupFile
} elseif ($List) {
    List-Backups
} else {
    Write-Host @"

GPU-SIM Registry Backup/Restore Script
=======================================

Usage:
    .\backup_restore.ps1 -Backup              Create new backup
    .\backup_restore.ps1 -List                List available backups
    .\backup_restore.ps1 -Restore -BackupFile <path>   Restore from backup

Examples:
    .\backup_restore.ps1 -Backup
    .\backup_restore.ps1 -List
    .\backup_restore.ps1 -Restore -BackupFile "backups\gpu_Video_20231215.reg"

"@ -ForegroundColor Cyan
}
