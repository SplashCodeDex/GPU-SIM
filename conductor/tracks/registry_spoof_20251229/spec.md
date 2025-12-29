# Specification: System-Wide Registry Spoofing

## 1. Overview
The goal of this track is to extend the "GPU illusion" beyond our application by modifying Windows Registry keys. This will cause standard Windows tools (dxdiag, Task Manager, Display Settings) to report the "spoofed" GPU name and VRAM instead of the real hardware.

## 2. Functional Requirements
*   **Hidden Trigger:** The "Install/Spoof" action must be hidden within the "System Information" dialog. It should not be obvious to an observer.
*   **On-Demand Elevation:** The application must trigger a Windows UAC (Administrator) prompt ONLY when the user clicks the hidden spoof button.
*   **Registry Targets:** The implementation must target keys used by Windows reporting tools, specifically:
    *   `AdapterString` (to change the reported GPU Name).
    *   `MemorySize` (to change the reported Dedicated Video Memory).
*   **Data Source:** The values written to the registry must come from the `config/gpu_config.json` file.
*   **Security:** The application must ensure it only modifies registry keys related to display adapters to avoid system instability.

## 3. Non-Functional Requirements
*   **Authenticity:** The UAC prompt should appear legitimate (associated with "NVIDIA Driver Setup" if possible, or clear about its purpose).
*   **Performance:** Registry operations must be fast and happen in the background to avoid UI hangs.

## 4. Acceptance Criteria
*   [ ] A hidden button/area in the "System Information" dialog exists to trigger the spoof.
*   [ ] Clicking the button triggers a UAC Administrator prompt.
*   [ ] After applying the spoof and restarting system tools (like Task Manager), the reported GPU name matches the one in `gpu_config.json`.
*   [ ] The reported VRAM in Windows Display Settings matches the one in `gpu_config.json`.
