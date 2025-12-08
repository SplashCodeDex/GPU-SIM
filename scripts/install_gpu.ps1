<#
.SYNOPSIS
    Install a virtual GPU profile into Windows registry.

.DESCRIPTION
    This script modifies Windows registry to create entries for a virtual GPU.
    The GPU will appear in Task Manager, DxDiag, and Windows Settings.

.PARAMETER Profile
    Name of the GPU profile to install (without .json extension).
    Available profiles: nvidia_gtx_780ti, nvidia_rtx_3080, amd_rx_6800xt

.PARAMETER ListProfiles
    List all available GPU profiles.

.PARAMETER DryRun
    Show what would be modified without making changes.

.EXAMPLE
    .\install_gpu.ps1 -Profile nvidia_rtx_3080
    Installs the RTX 3080 virtual GPU profile.

.EXAMPLE
    .\install_gpu.ps1 -ListProfiles
    Lists all available GPU profiles.

.NOTES
    REQUIRES ADMINISTRATOR PRIVILEGES!
    Always create a backup first: .\backup_restore.ps1 -Backup

    WARNING: Modifying system registry can cause system instability.
    Test in a virtual machine first!
#>

param(
    [string]$Profile = "",
    [switch]$ListProfiles,
    [switch]$DryRun
)

# Configuration
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$ProfilesDir = Join-Path $ProjectRoot "config\gpu_profiles"

# Registry paths
$DisplayClassPath = "HKLM:\SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}"

function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Get-AvailableProfiles {
    $profiles = Get-ChildItem -Path $ProfilesDir -Filter "*.json" -ErrorAction SilentlyContinue
    return $profiles
}

function Show-Profiles {
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "  Available GPU Profiles" -ForegroundColor Cyan
    Write-Host "========================================`n" -ForegroundColor Cyan

    $profiles = Get-AvailableProfiles

    if ($profiles.Count -eq 0) {
        Write-Host "[ERROR] No profiles found in: $ProfilesDir" -ForegroundColor Red
        return
    }

    foreach ($profileFile in $profiles) {
        $content = Get-Content $profileFile.FullName | ConvertFrom-Json
        $name = $content.name
        $vram = [math]::Round($content.vram_mb / 1024, 1)
        $driver = $content.driver_version

        Write-Host "  $($profileFile.BaseName)" -ForegroundColor Green
        Write-Host "    Name: $name" -ForegroundColor White
        Write-Host "    VRAM: ${vram} GB | Driver: $driver" -ForegroundColor Gray
        Write-Host ""
    }

    Write-Host "Usage: .\install_gpu.ps1 -Profile <profile_name>" -ForegroundColor Yellow
}

function Install-GPUProfile {
    param([string]$ProfileName)

    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "  GPU-SIM: Virtual GPU Installation" -ForegroundColor Cyan
    Write-Host "========================================`n" -ForegroundColor Cyan

    # Check admin
    if (-not (Test-Administrator)) {
        Write-Host "[ERROR] This script requires Administrator privileges!" -ForegroundColor Red
        Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
        return
    }

    # Load profile
    $profilePath = Join-Path $ProfilesDir "$ProfileName.json"
    if (-not (Test-Path $profilePath)) {
        Write-Host "[ERROR] Profile not found: $profilePath" -ForegroundColor Red
        Write-Host "Use -ListProfiles to see available profiles" -ForegroundColor Yellow
        return
    }

    $profileData = Get-Content $profilePath | ConvertFrom-Json
    Write-Host "[*] Loading profile: $($profileData.name)" -ForegroundColor Green
    Write-Host "    VRAM: $([math]::Round($profileData.vram_mb / 1024, 1)) GB" -ForegroundColor Gray
    Write-Host "    Driver: $($profileData.driver_version)" -ForegroundColor Gray

    if ($DryRun) {
        Write-Host "`n[DRY RUN] Would modify the following registry entries:" -ForegroundColor Yellow
    } else {
        Write-Host "`n[!] WARNING: This will modify your system registry!" -ForegroundColor Red
        Write-Host "[!] Make sure you have created a backup first!" -ForegroundColor Red

        $confirmation = Read-Host "`nHave you created a backup? Continue? (yes/no)"
        if ($confirmation -ne "yes") {
            Write-Host "`n[CANCELLED] Run: .\backup_restore.ps1 -Backup first" -ForegroundColor Yellow
            return
        }
    }

    # Find existing display adapter entries
    Write-Host "`n[*] Scanning for display adapter entries..." -ForegroundColor Yellow

    $adapterPaths = @()
    try {
        $subkeys = Get-ChildItem -Path $DisplayClassPath -ErrorAction Stop
        foreach ($key in $subkeys) {
            if ($key.PSChildName -match "^\d{4}$") {
                $adapterPaths += $key.PSPath
            }
        }
    } catch {
        Write-Host "[ERROR] Could not access display class registry: $_" -ForegroundColor Red
        return
    }

    if ($adapterPaths.Count -eq 0) {
        Write-Host "[ERROR] No display adapter entries found in registry" -ForegroundColor Red
        return
    }

    Write-Host "    Found $($adapterPaths.Count) adapter(s)" -ForegroundColor Green

    # Apply to first adapter (or create new one in future)
    $targetPath = $adapterPaths[0]
    Write-Host "`n[*] Target: $targetPath" -ForegroundColor Yellow

    # Registry entries to set
    $registryEntries = @{
        "DriverDesc" = $profileData.name
        "ProviderName" = $profileData.manufacturer
        "DriverVersion" = $profileData.driver_version
        "HardwareInformation.AdapterString" = $profileData.registry_entries."HardwareInformation.AdapterString"
        "HardwareInformation.ChipType" = $profileData.registry_entries."HardwareInformation.ChipType"
        "HardwareInformation.DACType" = $profileData.registry_entries."HardwareInformation.DACType"
        "HardwareInformation.MemorySize" = $profileData.registry_entries."HardwareInformation.MemorySize"
    }

    Write-Host "`n[*] Applying registry entries..." -ForegroundColor Yellow

    foreach ($entry in $registryEntries.GetEnumerator()) {
        if ($null -eq $entry.Value) { continue }

        if ($DryRun) {
            Write-Host "    [DRY] Would set: $($entry.Key) = $($entry.Value)" -ForegroundColor DarkYellow
        } else {
            try {
                if ($entry.Value -is [int] -or $entry.Value -is [long]) {
                    Set-ItemProperty -Path $targetPath -Name $entry.Key -Value $entry.Value -Type DWord -ErrorAction Stop
                } else {
                    Set-ItemProperty -Path $targetPath -Name $entry.Key -Value $entry.Value -Type String -ErrorAction Stop
                }
                Write-Host "    [OK] $($entry.Key)" -ForegroundColor Green
            } catch {
                Write-Host "    [WARN] Could not set $($entry.Key): $_" -ForegroundColor DarkYellow
            }
        }
    }

    if ($DryRun) {
        Write-Host "`n[DRY RUN COMPLETE] No changes were made" -ForegroundColor Yellow
    } else {
        Write-Host "`n========================================" -ForegroundColor Green
        Write-Host "  Installation Complete!" -ForegroundColor Green
        Write-Host "========================================" -ForegroundColor Green
        Write-Host "`n[!] IMPORTANT: Restart your computer for changes to take effect!" -ForegroundColor Cyan
        Write-Host "[!] To undo: Run .\backup_restore.ps1 -Restore -BackupFile <your_backup>" -ForegroundColor Cyan
    }
}

# Main execution
if ($ListProfiles) {
    Show-Profiles
} elseif ($Profile) {
    Install-GPUProfile -ProfileName $Profile
} else {
    Write-Host @"

GPU-SIM Virtual GPU Installation Script
========================================

Usage:
    .\install_gpu.ps1 -ListProfiles          Show available GPU profiles
    .\install_gpu.ps1 -Profile <name>        Install a GPU profile
    .\install_gpu.ps1 -Profile <name> -DryRun    Preview changes without applying

IMPORTANT:
    1. Run PowerShell as Administrator
    2. Create a backup first: .\backup_restore.ps1 -Backup
    3. Test in a virtual machine first!

Examples:
    .\install_gpu.ps1 -ListProfiles
    .\install_gpu.ps1 -Profile nvidia_rtx_3080 -DryRun
    .\install_gpu.ps1 -Profile nvidia_rtx_3080

"@ -ForegroundColor Cyan
}
