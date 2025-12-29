# Plan: Reality-Shield: Registry Persistence Service

## Phase 1: Startup Persistence Logic
- [x] Task: Implement `AutoStartService` [bcb4b40]
    - [x] Sub-task: Write logic to add/remove the application from `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`.
    - [x] Sub-task: Ensure the startup command includes a `--silent` flag to launch minimized to tray.
- [x] Task: Update `MainViewModel.cs` [bcb4b40]
    - [x] Sub-task: Add `IsAutoStartEnabled` property and bind it to a new menu item in "Desktop".
    - [x] Sub-task: Initialize property state by checking the registry key.
- [x] Task: Conductor - User Manual Verification 'Startup Persistence Logic' (Protocol in workflow.md) [bcb4b40]

## Phase 2: Periodic Enforcement (The Shield)
- [ ] Task: Implement `RealityShieldService`
    - [ ] Sub-task: Create a service that uses a `System.Timers.Timer` set to 60 seconds.
    - [ ] Sub-task: On each tick, call `RegistrySpoofService.ApplySpoof` with the current configuration.
- [ ] Task: Integrate Shield with App Lifecycle
    - [ ] Sub-task: Start the `RealityShieldService` in `App.xaml.cs` upon successful startup.
    - [ ] Sub-task: Handle the `--silent` argument in `App.xaml.cs` to prevent the main window from showing.
- [ ] Task: Conductor - User Manual Verification 'Periodic Enforcement (The Shield)' (Protocol in workflow.md)

## Phase 3: Admin-Enforced Logic
- [ ] Task: Automatic Elevation Flow
    - [ ] Sub-task: If the app starts and is NOT elevated, and `IsAutoStartEnabled` is true, trigger the self-elevation logic immediately.
- [ ] Task: Conductor - User Manual Verification 'Admin-Enforced Logic' (Protocol in workflow.md)

## Phase 4: Final Verification
- [ ] Task: Persistence Stress Test
    - [ ] Sub-task: Enable Auto-Start, restart the computer, and verify the app appears in the tray.
    - [ ] Sub-task: Use `regedit` to manually change the GPU name to "Fake GPU", wait 60 seconds, and verify it reverts to "GTX 1650".
- [ ] Task: Conductor - User Manual Verification 'Final Verification' (Protocol in workflow.md)
