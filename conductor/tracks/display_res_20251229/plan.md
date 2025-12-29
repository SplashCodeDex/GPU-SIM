# Plan: Display Resolution & Refresh Rate Simulation

## Phase 1: Data Model and Storage
- [x] Task: Update `GpuInformation` and `SimulationConfig` [eb8521d]
    - [x] Sub-task: Add `SelectedResolution` and `SelectedRefreshRate` properties to both classes.
    - [x] Sub-task: Update `SimulationService` to handle saving/loading these new persistence fields.
- [x] Task: Create Resolution Data Provider [eb8521d]
    - [x] Sub-task: Create a static helper to provide the "Elite" list of resolutions (2K, 1080p) and their supported refresh rates (60, 120, 144).
- [x] Task: Conductor - User Manual Verification 'Data Model and Storage' (Protocol in workflow.md) [eb8521d]

## Phase 2: ViewModels and Logic
- [ ] Task: Update `DisplayResolutionViewModel.cs`
    - [ ] Sub-task: Implement `ApplyCommand` logic to trigger the flicker and then the confirmation dialog.
    - [ ] Sub-task: Implement the 15-second countdown timer logic with a `Revert` action.
    - [ ] Sub-task: Inject `ISimulationService` to save the "confirmed" settings.
- [ ] Task: Conductor - User Manual Verification 'ViewModels and Logic' (Protocol in workflow.md)

## Phase 3: UI and UX (The Flicker)
- [ ] Task: Implement `FlickerService`
    - [ ] Sub-task: Create a service that opens a full-screen, top-most black `Window` for a specified duration.
- [ ] Task: Update `DisplayResolutionView.xaml`
    - [ ] Sub-task: Design the layout to match the NVIDIA "Change Resolution" screen (Resolution list, Refresh rate combo box).
- [ ] Task: Create `ConfirmationDialogView.xaml`
    - [ ] Sub-task: Design a small, authentic-looking dialog with the "Keep changes?" message and timer.
- [ ] Task: Conductor - User Manual Verification 'UI and UX (The Flicker)' (Protocol in workflow.md)

## Phase 4: Final Verification
- [ ] Task: Full UX Walkthrough
    - [ ] Sub-task: Select 144Hz, click Apply, verify the black screen duration, and confirm the timer dialog appears.
    - [ ] Sub-task: Verify that "No" or timeout reverts the selection, while "Yes" saves it to `gpu_config.json`.
- [ ] Task: Conductor - User Manual Verification 'Final Verification' (Protocol in workflow.md)
