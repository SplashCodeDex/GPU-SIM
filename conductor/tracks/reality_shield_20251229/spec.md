# Specification: Reality-Shield: Registry Persistence Service

## 1. Overview
The "Reality-Shield" is a background persistence mechanism designed to ensure that spoofed registry values (GPU Name, VRAM) are never reverted by the Windows operating system. It ensures the "lie" remains active even after reboots, hardware scans, or system updates.

## 2. Functional Requirements
*   **Startup Persistence:**
    *   The application must be able to add itself to the Windows "Run" registry key (`HKCU\Software\Microsoft\Windows\CurrentVersion\Run`) to ensure it starts automatically upon login.
*   **Periodic Enforcement:**
    *   Once running, the application must perform a "sweep" of target registry keys (GPU Name, VRAM) every 60 seconds.
    *   If the current registry values do not match the values in `config/gpu_config.json`, the application must silently overwrite them.
*   **Silent Operation:** All enforcement actions must be invisible to the user. No notifications or windows should appear during a sweep.
*   **Admin-Enforced Startup:** 
    *   When launched via the startup task, the application must automatically attempt to elevate to Administrator privileges (using the `--apply-spoof` background logic) to ensure it has write access to the registry.
*   **Stealth Launch:** When starting with Windows, the application should launch minimized to the system tray.

## 3. Non-Functional Requirements
*   **Resource Usage:** The periodic sweep must use negligible CPU and memory (less than 0.1%).
*   **Robustness:** The application must handle cases where the `config/gpu_config.json` is missing during a sweep by using the standard GTX 1650 defaults.

## 4. Acceptance Criteria
*   [ ] A toggle exists in the "Desktop" menu to "Enable Persistence (Auto-Start with Windows)".
*   [ ] Manually changing the registry value for `AdapterString` to something else results in it being corrected back to the spoofed value within 60 seconds.
*   [ ] Restarting the computer automatically launches the application in the system tray.
*   [ ] The application successfully reapplies the spoof upon startup after a reboot.
