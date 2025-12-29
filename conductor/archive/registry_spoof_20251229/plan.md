# Plan: System-Wide Registry Spoofing

## Phase 1: Registry Service Layer
- [x] Task: Define `IRegistrySpoofService` Interface [28a29d5]
    - [x] Sub-task: Create `IRegistrySpoofService.cs` with methods `ApplySpoof(GpuInformation info)` and `IsElevated()`.
- [x] Task: Implement `RegistrySpoofService` [28a29d5]
    - [x] Sub-task: Write logic to identify the correct Registry path (under `HKLM\SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}`).
    - [x] Sub-task: Implement `ApplySpoof` to update `HardwareInformation.AdapterString` and `HardwareInformation.qwMemorySize`.
    - [x] Sub-task: Implement self-elevation logic using `ProcessStartInfo` with the `"runas"` verb to trigger the UAC prompt if not already Admin.
- [x] Task: Conductor - User Manual Verification 'Registry Service Layer' (Protocol in workflow.md) [28a29d5]

## Phase 2: UI Integration (The Hidden Trigger)
- [x] Task: Update `SystemInfoView.xaml` [eb8521d]
    - [x] Sub-task: Add a hidden button or "Secret Click" area (e.g., double-clicking the NVIDIA Logo or a specific text label).
    - [x] Sub-task: Bind the interaction to a new `ApplyRegistrySpoofCommand`.
- [x] Task: Update `SystemInfoViewModel.cs` [eb8521d]
    - [x] Sub-task: Inject `IRegistrySpoofService`.
    - [x] Sub-task: Implement `ApplyRegistrySpoofCommand` to call the service with current GPU info.
    - [x] Sub-task: Add a "Success" notification mimicking a driver confirmation dialog.
- [x] Task: Conductor - User Manual Verification 'UI Integration (The Hidden Trigger)' (Protocol in workflow.md) [eb8521d]

## Phase 3: Final Verification
- [x] Task: System-Wide Verification [eb8521d]
    - [x] Sub-task: Run the app, trigger the hidden spoof, and confirm the UAC prompt appears.
    - [x] Sub-task: Open Windows Task Manager and verify the GPU name matches `gpu_config.json`.
    - [x] Sub-task: Open Windows Display Settings and verify the VRAM matches `gpu_config.json`.
- [x] Task: Conductor - User Manual Verification 'Final Verification' (Protocol in workflow.md) [eb8521d]
