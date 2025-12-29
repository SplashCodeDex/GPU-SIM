# Plan: NVIDIA Desktop Context Menu Simulation

## Phase 1: Service Layer Implementation
- [x] Task: Define `IContextMenuService` Interface [27e7861]
    - [x] Sub-task: Create `IContextMenuService.cs` with methods `IsEnabled()`, `Enable()`, and `Disable()`.
- [x] Task: Implement `ContextMenuService` [27e7861]
    - [x] Sub-task: Write logic to manage `HKEY_CLASSES_ROOT\DesktopBackground\Shell\NvidiaControlPanel`.
    - [x] Sub-task: Implement on-demand elevation using the `--apply-context-menu` argument pattern.
    - [x] Sub-task: Implement `IsEnabled()` to check if the registry keys currently exist.
- [x] Task: Conductor - User Manual Verification 'Service Layer Implementation' (Protocol in workflow.md) [27e7861]

## Phase 2: UI Integration and Persistence
- [x] Task: Update `MainViewModel.cs` [27e7861]
    - [x] Sub-task: Inject `IContextMenuService`.
    - [x] Sub-task: Update `IsContextMenuEnabled` property to call the service's Enable/Disable methods.
    - [x] Sub-task: Initialize `IsContextMenuEnabled` state from `IContextMenuService` on startup.
- [x] Task: Update `App.xaml.cs` [27e7861]
    - [x] Sub-task: Add a handler for the `--apply-context-menu` argument to perform the registry action and exit.
- [x] Task: Update `SimulationConfig` and `GpuInformation` [27e7861]
    - [x] Sub-task: Add `IsContextMenuEnabled` to the persistence models.
- [x] Task: Conductor - User Manual Verification 'UI Integration and Persistence' (Protocol in workflow.md) [27e7861]

## Phase 3: Final Verification
- [ ] Task: End-to-End Walkthrough
    - [ ] Sub-task: Toggle the context menu in the app, confirm UAC, and verify the item appears on the desktop.
    - [ ] Sub-task: Right-click desktop, click "NVIDIA Control Panel", and verify the app launches.
    - [ ] Sub-task: Toggle off and verify the item is removed.
- [ ] Task: Conductor - User Manual Verification 'Final Verification' (Protocol in workflow.md)
