# Plan: File-Based GPU Configuration for Static Spoofing

## Phase 1: Configuration Infrastructure
- [x] Task: Update `GpuInformation` Model [28a29d5]
    - [x] Sub-task: Write Unit Test verifying the model can hold new fields (BIOS, Bus, DirectX, IDs).
    - [x] Sub-task: Add properties for `BusSupport`, `BiosVersion`, `DirectXSupport`, `DeviceId`, and `VendorId` to `GpuInformation.cs`.
- [x] Task: Refactor `SystemInfoService` for File IO [28a29d5]
    - [x] Sub-task: Write Unit Test for `GetGpuInformation` that mocks a missing file and expects default values.
    - [x] Sub-task: Write Unit Test that mocks an existing `gpu_config.json` and expects values to match.
    - [x] Sub-task: Update `SystemInfoService.cs` to handle directory/file creation and JSON serialization/deserialization at `config/gpu_config.json`.
- [x] Task: Conductor - User Manual Verification 'Configuration Infrastructure' (Protocol in workflow.md) [28a29d5]

## Phase 2: Data Binding and Display
- [x] Task: Update ViewModels for Extended Info [28a29d5]
    - [x] Sub-task: Write Unit Test for `HomeViewModel` and `SystemInfoViewModel` ensuring they expose the new fields.
    - [x] Sub-task: Update `HomeViewModel.cs` and `SystemInfoViewModel.cs` to include the new properties from the updated model.
- [x] Task: Update Home and System Info Views [28a29d5]
    - [x] Sub-task: Update `HomeView.xaml` to display the new hardware details in the information card.
    - [x] Sub-task: Update `SystemInfoView.xaml` to include rows for BIOS, Bus, and DirectX versions.
- [x] Task: Conductor - User Manual Verification 'Data Binding and Display' (Protocol in workflow.md) [28a29d5]

## Phase 3: Final Verification
- [ ] Task: End-to-End Simulation Check
    - [ ] Sub-task: Delete the `config/` folder, run the app, and verify the GTX 1650 default is created.
    - [ ] Sub-task: Manually edit `gpu_config.json` to a different GPU (e.g., RTX 4090) and verify all UI elements update correctly on restart.
- [ ] Task: Conductor - User Manual Verification 'Final Verification' (Protocol in workflow.md)
