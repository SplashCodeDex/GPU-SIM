# Specification: NVIDIA Notification Tray Icon & Persistence

## 1. Overview
The goal of this track is to implement a persistent system tray icon for the NVIDIA Control Panel clone. This provides a permanent visual presence in the Windows taskbar, mimicking the behavior of the real NVIDIA driver and allowing the application to remain "running" in the background even when the main window is closed.

## 2. Functional Requirements
*   **System Tray Presence:** A green NVIDIA icon must appear in the Windows Notification Area (System Tray).
*   **Minimize to Tray:** Clicking the 'X' (Close) button on the main window must hide the window instead of exiting the application.
*   **Restore from Tray:** 
    *   Double-clicking the tray icon must restore the main window.
    *   Right-clicking the tray icon must show a context menu with an "NVIDIA Control Panel" option that restores the window.
*   **Exit Logic:** The application must only fully exit when the user selects "Exit" from the "File" menu or the tray icon's context menu.
*   **Manual Toggle:** The user can enable or disable the tray icon via the "Desktop > Show Notification Tray Icon" menu item.
*   **Persistence:** The "Show Notification Tray Icon" setting must be saved in `config/gpu_config.json`.

## 3. Non-Functional Requirements
*   **Authenticity:** The icon and context menu styling should match standard Windows tray behaviors.
*   **Resource Efficiency:** The background process should use minimal CPU and memory while minimized.

## 4. Acceptance Criteria
*   [ ] The NVIDIA icon is visible in the system tray upon app startup.
*   [ ] Closing the main window hides it to the tray.
*   [ ] Double-clicking the tray icon restores the window.
*   [ ] Right-clicking the icon shows a menu with "NVIDIA Control Panel" and "Exit".
*   [ ] Toggling the setting in the "Desktop" menu correctly adds/removes the tray icon and persists the choice.
