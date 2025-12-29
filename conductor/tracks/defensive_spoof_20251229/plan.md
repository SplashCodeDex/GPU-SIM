# Plan: Defensive Spoofing - Unselectable High-End Options

## Phase 1: Model & Logic Thresholds
- [x] Task: Update Display Models [08188f3]
    - [x] Sub-task: Create `RefreshRate.cs` model with `Value` (int) and `IsElite` (bool).
    - [x] Sub-task: Update `Resolution.cs` to use `ObservableCollection<RefreshRate>` and add an `IsElite` property.
- [x] Task: Update `ResolutionProvider.cs` [08188f3]
    - [x] Sub-task: Mark 2K resolutions as `IsElite = true`.
    - [x] Sub-task: Mark refresh rates > 60Hz as `IsElite = true`.
- [x] Task: Update `DisplayResolutionViewModel.cs` [08188f3]
    - [x] Sub-task: Add logic to intercept selection of Elite items and instead trigger the `ShowUpdateRequiredCommand`.
- [x] Task: Conductor - User Manual Verification 'Model & Logic Thresholds' (Protocol in workflow.md) [08188f3]

## Phase 2: The "Convincing Failure" UI
- [x] Task: Implement `FakeUpdateViewModel.cs` [e4f59fe]
    - [x] Sub-task: Implement a timer that advances a `ProgressValue` to exactly 19 and then stops.
    - [x] Sub-task: Implement `ErrorMessage` visibility logic after the 19% stall.
- [x] Task: Create `FakeUpdateView.xaml` [e4f59fe]
    - [x] Sub-task: Design an authentic NVIDIA-branded dialog with a `ProgressBar` and status labels.
    - [x] Sub-task: Ensure no clickable links are present in the final error state.
- [x] Task: Update `App.xaml.cs` [e4f59fe]
    - [x] Sub-task: Handle `--fake-update` argument to launch the `FakeUpdateView` as a standalone Admin process.
- [x] Task: Conductor - User Manual Verification 'The "Convincing Failure" UI' (Protocol in workflow.md) [e4f59fe]

## Phase 3: UI Styling & Wiring
- [x] Task: Update `DisplayResolutionView.xaml` [e4f59fe]
    - [x] Sub-task: Use `ItemContainerStyle` with `DataTriggers` to dim (Opacity 0.5) and disable Elite items in the ListBox and ComboBox.
    - [x] Sub-task: Bind the click/selection of disabled items to the fake update flow.
- [x] Task: Conductor - User Manual Verification 'UI Styling & Wiring' (Protocol in workflow.md) [e4f59fe]

## Phase 4: Final Verification
- [ ] Task: Defensive Walkthrough
    - [ ] Sub-task: Try to select 144Hz, confirm UAC "NVIDIA Web Helper" appears.
    - [ ] Sub-task: Verify the progress bar stalls at 19% and shows the "Connection Timed Out" error with manual instructions.
- [ ] Task: Conductor - User Manual Verification 'Final Verification' (Protocol in workflow.md)
