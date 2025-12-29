# Specification: Display Resolution & Refresh Rate Simulation

## 1. Overview
The goal of this track is to implement a high-fidelity "Change Resolution" page within the Control Panel. This page will allow the user to select "fake" high-end display settings (up to 2K resolution and 144Hz refresh rate) and simulate the physical experience of a hardware mode switch.

## 2. Functional Requirements
*   **Resolution List:** Provide a list of simulated resolutions, including:
    *   2560 x 1440 (2K)
    *   1920 x 1080 (HD)
*   **Refresh Rate List:** Provide a list of simulated refresh rates, including:
    *   60Hz
    *   120Hz
    *   144Hz
*   **The "Apply" Flow:**
    1.  User clicks "Apply".
    2.  **Screen Flicker:** The app triggers a full-screen black overlay for 1.5 seconds to mimic a hardware sync.
    3.  **Confirmation Dialog:** After the flicker, show a dialog: *"Your desktop has been reconfigured. Do you want to keep these changes? Reverting in [X] seconds."*
    4.  **Timer:** If the user doesn't click "Yes" within 15 seconds, "revert" the UI state to the previous selection.
*   **Persistence:** The "selected" resolution/refresh rate should be saved in `config/gpu_config.json` so it stays static even after a restart.

## 3. Non-Functional Requirements
*   **UX Realism:** The black screen must cover all monitors if possible (or at least the primary one) to prevent the "friend" from seeing the real desktop during the switch.
*   **Visual Fidelity:** The "Change Resolution" UI layout must precisely mirror the original NVIDIA Control Panel layout (list of resolutions on the left, properties on the right).

## 4. Acceptance Criteria
*   [ ] A functional "Change Resolution" page exists in the navigation tree.
*   [ ] Clicking "Apply" triggers a 1.5-second black screen.
*   [ ] The "Keep changes?" dialog appears with a functioning 15-second countdown.
*   [ ] The selected resolution is correctly saved and displayed in the app upon restart.
