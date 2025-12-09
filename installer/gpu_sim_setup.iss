; ============================================================
; GPU-SIM + NVIDIA Control Panel Installer
; Inno Setup Script - Professional Windows Installer
; ============================================================
; To compile this installer, install Inno Setup from:
; https://jrsoftware.org/isinfo.php
; Then open this file in Inno Setup Compiler and click Build
; ============================================================

#define AppName "GPU-SIM"
#define AppVersion "1.0.0"
#define AppPublisher "CodeDeX Development"
#define AppURL "https://github.com/CodeDeX/GPU-SIM"
#define AppExeName "gpu_sim.exe"
#define NvidiaExeName "nvidia_control_panel.exe"
#define GFExeName "GeForceExperience.exe"

[Setup]
; Basic installer info
AppId={{7E5F3D2A-8B4C-4A1E-9D6F-2C3E5A8B1D4F}
AppName={#AppName}
AppVersion={#AppVersion}
AppVerName={#AppName} {#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppURL}
AppSupportURL={#AppURL}
AppUpdatesURL={#AppURL}

; Installation directories
DefaultDirName={autopf}\GPU-SIM
DefaultGroupName={#AppName}
DisableProgramGroupPage=yes

; Output settings
OutputDir=installer\output
OutputBaseFilename=GPU-SIM_Setup_{#AppVersion}
SetupIconFile=Agenda\512x512.ico
UninstallDisplayIcon={app}\{#AppExeName}
Compression=lzma2/ultra64
SolidCompression=yes

; Appearance & Behavior
WizardStyle=modern
WizardSizePercent=110
ShowLanguageDialog=auto
DisableWelcomePage=no
LicenseFile=LICENSE
InfoBeforeFile=README.md

; Privileges
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog

; Windows version requirements
MinVersion=10.0

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Types]
Name: "full"; Description: "Full installation (GPU-SIM + NVIDIA Control Panel)"
Name: "nvidia_only"; Description: "NVIDIA Control Panel only"
Name: "custom"; Description: "Custom installation"; Flags: iscustom

[Components]
Name: "main"; Description: "GPU-SIM Core Application"; Types: full
Name: "nvidia"; Description: "NVIDIA Control Panel Replica"; Types: full nvidia_only
Name: "geforce"; Description: "GeForce Experience Replica"; Types: full
Name: "vdd"; Description: "Virtual Display Driver (for DxDiag/Task Manager spoofing)"; Types: full
Name: "shortcuts"; Description: "Desktop Shortcuts"; Types: full nvidia_only
Name: "contextmenu"; Description: "Add to Windows Right-Click Menu"; Types: full

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce; Components: shortcuts
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Components: shortcuts
Name: "startupicon"; Description: "Start NVIDIA Control Panel with Windows"; GroupDescription: "Startup Options"; Flags: unchecked; Components: nvidia
Name: "contextmenu"; Description: "Add NVIDIA Control Panel to desktop right-click menu"; GroupDescription: "Context Menu Integration"; Flags: unchecked; Components: contextmenu
Name: "testsigning"; Description: "Enable Test Signing Mode (required for VDD, needs reboot)"; GroupDescription: "Driver Options"; Flags: unchecked; Components: vdd

[Files]
; Main GPU-SIM application
Source: "dist\gpu_sim\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: main
Source: "config\*"; DestDir: "{app}\config"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: main nvidia

; NVIDIA Control Panel
Source: "dist\nvidia_control_panel\*"; DestDir: "{app}\nvidia_panel"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: nvidia

; GeForce Experience
Source: "dist\geforce_experience\*"; DestDir: "{app}\geforce_experience"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: geforce

; Virtual Display Driver (VDD)
Source: "drivers\vdd\Virtual-Display-Driver\Virtual Display Driver (HDR)\MttVDD\x64\Release\MttVDD\*"; DestDir: "{app}\vdd"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: vdd
Source: "injector\fakenvapi\build\src\nvapi64.dll"; DestDir: "{app}\bypass"; Flags: ignoreversion; Components: vdd

; Assets
Source: "Agenda\512x512.png"; DestDir: "{app}\assets"; Flags: ignoreversion
Source: "Agenda\512x512.ico"; DestDir: "{app}\assets"; Flags: ignoreversion; Check: FileExists('Agenda\512x512.ico')

; Documentation
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: "CHANGELOG.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Start Menu shortcuts
Name: "{group}\GPU-SIM"; Filename: "{app}\{#AppExeName}"; Components: main
Name: "{group}\NVIDIA Control Panel"; Filename: "{app}\nvidia_panel\{#NvidiaExeName}"; Components: nvidia
Name: "{group}\GeForce Experience"; Filename: "{app}\geforce_experience\{#GFExeName}"; Components: geforce
Name: "{group}\{cm:UninstallProgram,{#AppName}}"; Filename: "{uninstallexe}"
Name: "{group}\Documentation\README"; Filename: "{app}\README.md"
Name: "{group}\Documentation\Changelog"; Filename: "{app}\CHANGELOG.md"

; Desktop shortcuts
Name: "{autodesktop}\GPU-SIM"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon; Components: main
Name: "{autodesktop}\NVIDIA Control Panel"; Filename: "{app}\nvidia_panel\{#NvidiaExeName}"; Tasks: desktopicon; Components: nvidia
Name: "{autodesktop}\GeForce Experience"; Filename: "{app}\geforce_experience\{#GFExeName}"; Tasks: desktopicon; Components: geforce

; Quick Launch
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\GPU-SIM"; Filename: "{app}\{#AppExeName}"; Tasks: quicklaunchicon; Components: main

; Startup
Name: "{userstartup}\NVIDIA Control Panel"; Filename: "{app}\nvidia_panel\{#NvidiaExeName}"; Tasks: startupicon; Components: nvidia

[Registry]
; NVIDIA Control Panel - Add to right-click context menu
Root: HKCR; Subkey: "Directory\Background\shell\NVIDIAControlPanel"; ValueType: string; ValueName: ""; ValueData: "NVIDIA Control Panel"; Flags: uninsdeletekey; Tasks: contextmenu
Root: HKCR; Subkey: "Directory\Background\shell\NVIDIAControlPanel"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\nvidia_panel\{#NvidiaExeName},0"; Tasks: contextmenu
Root: HKCR; Subkey: "Directory\Background\shell\NVIDIAControlPanel\command"; ValueType: string; ValueName: ""; ValueData: """{app}\nvidia_panel\{#NvidiaExeName}"""; Tasks: contextmenu

; App registration
Root: HKLM; Subkey: "SOFTWARE\GPU-SIM"; ValueType: string; ValueName: "InstallPath"; ValueData: "{app}"; Flags: uninsdeletekey
Root: HKLM; Subkey: "SOFTWARE\GPU-SIM"; ValueType: string; ValueName: "Version"; ValueData: "{#AppVersion}"

[Run]
; Enable test signing mode if selected (requires reboot)
Filename: "bcdedit"; Parameters: "/set testsigning on"; Flags: runhidden; Tasks: testsigning

; Install VDD driver using pnputil
Filename: "pnputil"; Parameters: "/add-driver ""{app}\vdd\MttVDD.inf"" /install"; Flags: runhidden; Components: vdd

; Post-installation options
Filename: "{app}\{#AppExeName}"; Description: "{cm:LaunchProgram,GPU-SIM}"; Flags: nowait postinstall skipifsilent; Components: main
Filename: "{app}\nvidia_panel\{#NvidiaExeName}"; Description: "{cm:LaunchProgram,NVIDIA Control Panel}"; Flags: nowait postinstall skipifsilent unchecked; Components: nvidia
Filename: "{app}\geforce_experience\{#GFExeName}"; Description: "{cm:LaunchProgram,GeForce Experience}"; Flags: nowait postinstall skipifsilent unchecked; Components: geforce

[UninstallRun]
; Clean up on uninstall
Filename: "taskkill"; Parameters: "/f /im {#AppExeName}"; Flags: runhidden; RunOnceId: "KillGPUSIM"
Filename: "taskkill"; Parameters: "/f /im {#NvidiaExeName}"; Flags: runhidden; RunOnceId: "KillNVIDIA"
Filename: "taskkill"; Parameters: "/f /im {#GFExeName}"; Flags: runhidden; RunOnceId: "KillGFE"

[UninstallDelete]
; Remove config files on uninstall
Type: filesandordirs; Name: "{app}\config"
Type: filesandordirs; Name: "{app}\logs"

[Messages]
WelcomeLabel1=Welcome to the GPU-SIM Setup Wizard
WelcomeLabel2=This will install GPU-SIM {#AppVersion} and the NVIDIA Control Panel replica on your computer.%n%nGPU-SIM allows you to simulate different GPU configurations for testing and demonstration purposes.%n%n⚠️ IMPORTANT: This software modifies system registry values. Use in a virtual machine or create a system restore point before installation.

[Code]
// Check if running in admin mode for context menu tasks
function InitializeSetup(): Boolean;
begin
  Result := True;
  // Display a warning about registry modifications
  if MsgBox('GPU-SIM modifies Windows Registry to simulate GPU information.' + #13#10 + #13#10 +
            'RECOMMENDED: Run this in a Virtual Machine or create a System Restore Point before proceeding.' + #13#10 + #13#10 +
            'Do you want to continue?', mbConfirmation, MB_YESNO) = IDNO then
  begin
    Result := False;
  end;
end;

// Cleanup any running processes before uninstall
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  ResultCode: Integer;
begin
  if CurUninstallStep = usUninstall then
  begin
    // Kill running applications
    Exec('taskkill', '/f /im gpu_sim.exe', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
    Exec('taskkill', '/f /im nvidia_control_panel.exe', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
  end;
end;

// Check if NSIS/previous version exists
function IsPreviousVersionInstalled(): Boolean;
begin
  Result := RegKeyExists(HKLM, 'SOFTWARE\GPU-SIM');
end;

// Custom page for GPU profile selection (future enhancement)
procedure InitializeWizard();
var
  InfoPage: TNewNotebookPage;
begin
  // Can add custom pages here for GPU profile selection
  // This is a placeholder for future enhancement
end;
