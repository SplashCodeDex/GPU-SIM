# Specification: Defensive Spoofing - Unselectable High-End Options

## 1. Overview
The goal of this track is to implement a robust "defensive" UI strategy. We will show high-end hardware capabilities (like 144Hz and 2K resolution) to impress the observer, but prevent them from being selected. This avoids exposing real physical hardware limits while reinforcing the "installed driver" illusion via a convincing, but intentionally failing, update flow.

## 2. Functional Requirements
*   **Visual Representation:** 
    *   Resolutions above 1080p and refresh rates above 60Hz must be visible in the "Change Resolution" page.
    *   These "Elite" options must use the standard Windows **grayed-out** style (light gray text, slightly transparent).
*   **Interaction Logic:** 
    *   Elite items must be **unselectable**.
    *   Clicking a grayed-out item must trigger a "NVIDIA Update Required" dialog.
*   **The "Convincing Failure" Flow:**
    1.  **User Trigger:** Click a locked item or an "Update" button in the dialog.
    2.  **UAC Elevation:** Trigger a Windows Admin prompt branded as *"NVIDIA Web Helper"* or *"NVIDIA Driver Update Service"*.
    3.  **Progress Simulation:** Show a modal dialog with a "Downloading update package..." progress bar.
    4.  **The 19% Stall:** The progress bar must move slowly and stop exactly at **19%**.
    5.  **Timeout Error:** After stalling at 19% for 3-5 seconds, display an error message: *"Connection to NVIDIA update server timed out. Please visit the official website and download the latest driver manually."*
    6.  **No Redirects:** The error dialog must NOT contain any clickable links or buttons that open a web browser, to prevent further investigation by the friend.
*   **Threshold Management:** Settings exceeding physical hardware limits are defined as "Elite" Tier within `gpu_config.json`.

## 3. Non-Functional Requirements
*   **Deception Quality:** The UAC prompt and error dialogs must use authentic NVIDIA branding and icons.
*   **Enforcement:** The unselectable state must be hard-coded into the `DisplayResolutionViewModel` logic to prevent accidental selection via keyboard or other means.

## 4. Acceptance Criteria
*   [ ] 144Hz and 2K resolutions appear dimmed and cannot be selected.
*   [ ] Clicking a dimmed item triggers the UAC prompt branded as "NVIDIA Web Helper".
*   [ ] The update progress bar stalls at 19% and then shows the "Connection Timed Out" error.
*   [ ] The final error message provides manual instructions but provides no clickable links.
