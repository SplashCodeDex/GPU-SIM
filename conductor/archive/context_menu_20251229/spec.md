# Specification: NVIDIA Desktop Context Menu Simulation

## 1. Overview
The goal of this track is to add an authentic "NVIDIA Control Panel" entry to the Windows Desktop right-click context menu. This entry will link directly to our application, providing a realistic entry point for an observer and matching the behavior of the real NVIDIA driver software.

## 2. Functional Requirements
*   **Manual Toggle:** The user can enable or disable the desktop context menu via the "Desktop" menu in the application's menu bar.
*   **On-Demand Elevation:** When the user toggles the setting, the application must trigger a Windows UAC (Administrator) prompt to perform the registry modification.
*   **Registry Implementation:**
    *   **Enable:** Create keys under `HKEY_CLASSES_ROOT\DesktopBackground\Shell\NvidiaControlPanel`.
    *   **Icon:** Set the `Icon` value to the path of the application's executable.
    *   **Command:** Set the `command` sub-key to launch the application's executable.
    *   **Disable:** Delete the `NvidiaControlPanel` key from the registry.
*   **Wording:** The menu entry must read exactly "NVIDIA Control Panel".
*   **State Persistence:** The toggle state (Enabled/Disabled) must be saved in `config/gpu_config.json`.

## 3. Non-Functional Requirements
*   **Reliability:** The application must correctly identify its own file path, even if the executable has been renamed or moved.
*   **Silent Child Process:** Use the same `--apply-context-menu` (or similar) hidden argument pattern to perform the Admin action in a separate background process.

## 4. Acceptance Criteria
*   [ ] Toggling "Add Desktop Context Menu" in the app triggers a UAC prompt.
*   [ ] When enabled, right-clicking the Windows Desktop shows "NVIDIA Control Panel" with the correct icon.
*   [ ] Clicking the desktop menu item successfully launches the application.
*   [ ] When disabled, the entry is immediately removed from the Windows Desktop context menu.
*   [ ] The setting is remembered after the app is closed and restarted.
