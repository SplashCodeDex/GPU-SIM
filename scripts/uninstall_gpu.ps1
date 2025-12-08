<#
.SYNOPSIS
    Uninstall/revert virtual GPU changes from Windows registry.

.DESCRIPTION
    This script restores the original GPU registry entries by applying
    a previously created backup. It effectively removes the virtual GPU.

.PARAMETER BackupFile
    Path to the backup file to restore.

.PARAMETER Latest
    Automatically use the latest backup file.

.EXAMPLE
    .\uninstall_gpu.ps1 -Latest
    Restores from the most recent backup.

.EXAMPLE
    .\uninstall_gpu.ps1 -BackupFile "backups\gpu_backup.reg"
    Restores from specified backup.

.NOTES
    Requires Administrator privileges.
    Restart required after uninstallation.
#>

param(
    [string]$BackupFile = "",
    [switch]$Latest
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$BackupDir = Join-Path $ProjectRoot "backups"

function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Get-LatestBackup {
    $backups = Get-ChildItem -Path $BackupDir -Filter "*.reg" -ErrorAction SilentlyContinue |
               Sort-Object LastWriteTime -Descending

    if ($backups.Count -gt 0) {
        return $backups[0].FullName
    }
    return $null
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  GPU-SIM: Virtual GPU Uninstallation" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

if (-not (Test-Administrator)) {
    Write-Host "[ERROR] This script requires Administrator privileges!" -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    exit 1
}

# Determine backup file to use
$restoreFile = ""

if ($Latest) {
    $restoreFile = Get-LatestBackup
    if (-not $restoreFile) {
        Write-Host "[ERROR] No backup files found in: $BackupDir" -ForegroundColor Red
        Write-Host "Cannot uninstall without a backup to restore from." -ForegroundColor Yellow
        exit 1
    }
    Write-Host "[*] Using latest backup: $restoreFile" -ForegroundColor Green
} elseif ($BackupFile) {
    if (-not [System.IO.Path]::IsPathRooted($BackupFile)) {
        $restoreFile = Join-Path $ProjectRoot $BackupFile
    } else {
        $restoreFile = $BackupFile
    }

    if (-not (Test-Path $restoreFile)) {
        Write-Host "[ERROR] Backup file not found: $restoreFile" -ForegroundColor Red
        exit 1
    }
    Write-Host "[*] Using backup: $restoreFile" -ForegroundColor Green
} else {
    Write-Host @"
Usage:
    .\uninstall_gpu.ps1 -Latest                   Use most recent backup
    .\uninstall_gpu.ps1 -BackupFile <path>        Use specific backup

Available backups:
"@ -ForegroundColor Yellow

    $backups = Get-ChildItem -Path $BackupDir -Filter "*.reg" -ErrorAction SilentlyContinue |
               Sort-Object LastWriteTime -Descending | Select-Object -First 5

    foreach ($b in $backups) {
        Write-Host "  - $($b.Name)" -ForegroundColor Gray
    }
    exit 0
}

# Confirm and restore
Write-Host "`n[!] WARNING: This will restore registry from backup!" -ForegroundColor Red
Write-Host "[!] This will remove the virtual GPU configuration." -ForegroundColor Red

$confirmation = Read-Host "`nContinue with uninstallation? (yes/no)"
if ($confirmation -ne "yes") {
    Write-Host "`n[CANCELLED] Uninstallation cancelled" -ForegroundColor Yellow
    exit 0
}

Write-Host "`n[*] Restoring registry..." -ForegroundColor Yellow

try {
    reg import $restoreFile
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n========================================" -ForegroundColor Green
        Write-Host "  Uninstallation Complete!" -ForegroundColor Green
        Write-Host "========================================" -ForegroundColor Green
        Write-Host "`n[!] IMPORTANT: Restart your computer for changes to take effect!" -ForegroundColor Cyan
    } else {
        Write-Host "[ERROR] Registry restore failed" -ForegroundColor Red
    }
} catch {
    Write-Host "[ERROR] Failed to restore registry: $_" -ForegroundColor Red
}
