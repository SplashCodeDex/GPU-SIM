# Specification: Enhance Adjust Image Settings with Visual Fidelity & Persistence

## 1. Overview
The goal of this track is to refine the "Adjust Image Settings with Preview" page. We will make the 3D preview reactive to user choices (Performance vs. Quality) and ensure all selections are persisted to the `gpu_config.json` file.

## 2. Functional Requirements
*   **Visual Fidelity Simulation:**
    *   **Performance Mode:** Apply a "Pixelation" or "Blur" effect to the 3D logo and slow down the rotation animation to simulate a struggling/low-res GPU.
    *   **Quality Mode:** Display the 3D logo with high-resolution textures, smooth anti-aliasing, and a fluid rotation animation.
    *   **Balanced Mode:** A mid-point between the two.
*   **Two-Way Synchronization:**
    *   The `Slider` must be perfectly synced with the "Performance/Balanced/Quality" RadioButtons.
*   **The "Apply" Flow:**
    1.  User clicks "Apply".
    2.  Show a "Loading" cursor for 1 second.
    3.  Save the current state (Selection mode and Preference level) to `config/gpu_config.json`.
    4.  Show a non-intrusive notification: *"3D Settings Applied"*.
*   **Persistence:** Upon app startup, the page must load its state from `gpu_config.json`.

## 3. Non-Functional Requirements
*   **Smooth Transitions:** The visual effects (pixelation) should transition smoothly when the slider moves.
*   **Performance:** The pixelation shader/effect must not actually slow down the app's real performance.

## 4. Acceptance Criteria
*   [ ] Moving the slider to "Performance" visibly pixelates the spinning logo.
*   [ ] Rotation speed decreases in "Performance" mode and increases in "Quality" mode.
*   [ ] Clicking "Apply" shows a loading cursor and then a "Success" message.
*   [ ] Settings are correctly saved to `gpu_config.json` and reloaded on next launch.
