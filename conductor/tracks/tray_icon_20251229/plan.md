# Plan: NVIDIA Notification Tray Icon & Persistence

## Phase 1: Tray Service Implementation
- [x] Task: Create `ITrayIconService` Interface [c3baf28]
    - [x] Sub-task: Define methods `Show()`, `Hide()`, and `SetVisibility(bool visible)`.
- [x] Task: Implement `TrayIconService` [c3baf28]
    - [x] Sub-task: Use the standard WinForms NotifyIcon wrapper to manage the tray icon.
    - [x] Sub-task: Add the authentic green NVIDIA icon to the tray.
    - [x] Sub-task: Implement the context menu with "NVIDIA Control Panel" and "Exit" commands.
- [x] Task: Conductor - User Manual Verification 'Tray Service Implementation' (Protocol in workflow.md) [c3baf28]

## Phase 2: Application Lifecycle & Integration
- [ ] Task: Update `App.xaml.cs`
    - [ ] Sub-task: Handle the `SessionEnding` or `Exit` events to ensure clean tray icon removal.
    - [ ] Sub-task: Implement the "Single Instance" logic if necessary, or ensure restoring from tray works correctly.
- [ ] Task: Update `MainWindow.xaml.cs`
    - [ ] Sub-task: Override `OnClosing` to hide the window and cancel the close event unless a full exit is requested.
- [ ] Task: Update `MainViewModel.cs`
    - [ ] Sub-task: Inject `ITrayIconService`.
    - [ ] Sub-task: Bind the "Show Notification Tray Icon" menu toggle to the service.
    - [ ] Sub-task: Initialize tray state from `gpu_config.json`.
- [ ] Task: Conductor - User Manual Verification 'Application Lifecycle & Integration' (Protocol in workflow.md)

## Phase 3: Final Verification
- [ ] Task: Full UX Walkthrough
    - [ ] Sub-task: Launch app, verify tray icon presence.
    - [ ] Sub-task: Close window, verify app still runs in tray.
    - [ ] Sub-task: Restore from tray, toggle off in settings, and verify removal.
- [ ] Task: Conductor - User Manual Verification 'Final Verification' (Protocol in workflow.md)
