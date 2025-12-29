# Plan: Enhance Adjust Image Settings with Visual Fidelity & Persistence

## Phase 1: Persistence and Logic
- [x] Task: Update `GpuInformation` and `SimulationConfig` [27e7861]
    - [x] Sub-task: Add properties for `ImageSettingsMode` (enum/string) and `PreferenceLevel` (int).
    - [x] Sub-task: Update `SimulationService` to handle saving/loading these fields.
- [x] Task: Refactor `AdjustImageSettingsViewModel.cs` [27e7861]
    - [x] Sub-task: Write Unit Test for slider-to-radio synchronization.
    - [x] Sub-task: Implement two-way binding logic for the Preference Slider (0=Performance, 1=Balanced, 2=Quality).
    - [x] Sub-task: Implement `ApplyCommand` with 1-second delay and persistence call.
- [x] Task: Conductor - User Manual Verification 'Persistence and Logic' (Protocol in workflow.md) [27e7861]

## Phase 2: Visual Effects (The "WOW" Factor)
- [x] Task: Implement Pixelation Shader/Effect [aaa9485]
    - [x] Sub-task: Create a simple WPF `ShaderEffect` or use a `VisualBrush` scaling trick to simulate pixelation.
- [x] Task: Bind Effects to ViewModel [aaa9485]
    - [x] Sub-task: Expose `PixelationAmount` and `RotationDuration` properties in the ViewModel.
    - [x] Sub-task: Update `AdjustImageSettingsView.xaml` to bind the 3D logo's effect and animation duration to these properties.
- [x] Task: Conductor - User Manual Verification 'Visual Effects (The "WOW" Factor)' (Protocol in workflow.md) [aaa9485]

## Phase 3: Final Verification
- [x] Task: Full UX Walkthrough [7dc4507]
    - [x] Sub-task: Move slider to Performance, verify logo looks "worse" and spins slower.
    - [x] Sub-task: Click Apply, wait for cursor change, restart app, and verify settings persisted.
- [x] Task: Conductor - User Manual Verification 'Final Verification' (Protocol in workflow.md) [7dc4507]
