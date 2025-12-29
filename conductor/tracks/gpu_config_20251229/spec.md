# Specification: File-Based GPU Configuration for Static Spoofing

## 1. Overview
This track enables "Pre-flight Configuration" by moving hardware definitions from hardcoded strings to an external configuration file. This allows the user to define the GPU identity *before* a demonstration, ensuring the application presents a consistent and static illusion.

## 2. Functional Requirements
*   **File Location:** The application must look for configuration at `config/gpu_config.json` relative to the executable.
*   **Data Schema:** The JSON must support the following fields:
    *   `GpuName` (e.g., "NVIDIA GeForce GTX 1650")
    *   `DriverVersion` (e.g., "536.23")
    *   `VideoMemory` (e.g., "4096 MB GDDR5")
    *   `BusSupport` (e.g., "PCI Express x16 Gen 3")
    *   `BiosVersion` (e.g., "90.06.33.00.70")
    *   `DirectXSupport` (e.g., "12 Ultimate")
    *   `DeviceId` (e.g., "1F82")
    *   `VendorId` (e.g., "10DE")
*   **Initialization Logic:**
    *   If the `config/` directory or `gpu_config.json` file is missing, the app must automatically create them.
    *   The default generated configuration must be for an "NVIDIA GeForce GTX 1650".
    *   If the file is corrupted, the app must silently overwrite it with the default values to ensure it always opens successfully.
*   **Integration:** The `SystemInfoService` must be updated to use this file as its primary source of truth.

## 3. Non-Functional Requirements
*   **Silent Operation:** No "Config loaded" popups. The process must be invisible to the end observer.
*   **Error Masking:** Any IO errors during loading should be handled internally to prevent "File Not Found" exceptions from being visible.

## 4. Acceptance Criteria
*   [ ] Deleting the `config/` folder causes the app to regenerate a default GTX 1650 config.
*   [ ] Modifying `config/gpu_config.json` and restarting the app correctly updates the details in the Status Bar, Home View, and System Information dialog.
*   [ ] All new fields (BIOS, Bus, etc.) are visible in the System Information dialog.
