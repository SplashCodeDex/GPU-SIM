# Plan: NVIDIA Notification Tray Icon & Persistence

## Phase 1: Tray Service Implementation
- [x] Task: Create `ITrayIconService` Interface [5c0204c]
    - [x] Sub-task: Define methods `Show()`, `Hide()`, and `SetVisibility(bool visible)`.
- [x] Task: Implement `TrayIconService` [5c0204c]
    - [x] Sub-task: Use the standard WinForms NotifyIcon wrapper to manage the tray icon.
    - [x] Sub-task: Add the authentic green NVIDIA icon to the tray.
    - [x] Sub-task: Implement the context menu with "NVIDIA Control Panel" and "Exit" commands.
- [x] Task: Conductor - User Manual Verification 'Tray Service Implementation' (Protocol in workflow.md) [5c0204c]

## Phase 2: Application Lifecycle & Integration
- [x] Task: Update `App.xaml.cs` [5c0204c]
    - [x] Sub-task: Handle the `SessionEnding` or `Exit` events to ensure clean tray icon removal.
    - [x] Sub-task: Implement the "Single Instance" logic if necessary, or ensure restoring from tray works correctly.
- [x] Task: Update `MainWindow.xaml.cs` [5c0204c]
    - [x] Sub-task: Override `OnClosing` to hide the window and cancel the close event unless a full exit is requested.
- [x] Task: Update `MainViewModel.cs` [5c0204c]
    - [x] Sub-task: Inject `ITrayIconService`.
    - [x] Sub-task: Bind the "Show Notification Tray Icon" menu toggle to the service.
    - [x] Sub-task: Initialize tray state from `gpu_config.json`.
- [x] Task: Conductor - User Manual Verification 'Application Lifecycle & Integration' (Protocol in workflow.md) [5c0204c]

## Phase 3: Final Verification
- [x] Task: Full UX Walkthrough [bcb4b40]
    - [x] Sub-task: Launch app, verify tray icon presence.
    - [x] Sub-task: Close window, verify app still runs in tray.
    - [x] Sub-task: Restore from tray, toggle off in settings, and verify removal.
- [x] Task: Conductor - User Manual Verification 'Final Verification' (Protocol in workflow.md) [bcb4b40]
