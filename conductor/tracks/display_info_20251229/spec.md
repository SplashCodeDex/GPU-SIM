# Specification: Display Information Feature

## 1. Overview
The goal of this track is to implement the functionality to display "spoofed" GPU information within the main view of the NVIDIA Control Panel clone. This is critical for the "prank" aspect, as it provides visual confirmation to the user (and their target) that the "fake" hardware is recognized.

## 2. Functional Requirements
*   **Data Source:** The application must retrieve GPU data (Name, VRAM, Driver Version) from a configurable `SystemInfoService`, NOT from real hardware.
*   **Display:** The UI must display these values in a layout that mimics the "System Information" or main landing page of the original Control Panel.
*   **Default Values:** The initial configuration should default to a "NVIDIA GeForce GTX 1650" with 4GB of VRAM.
*   **MVVM Compliance:** Data must be bound from a `MainViewModel` (or dedicated `SystemInfoViewModel`) to the View.

## 3. Non-Functional Requirements
*   **Visual Fidelity:** The text styling (font, color) and layout must match the original application.
*   **Zero Code-Behind:** No logic in `.xaml.cs` files.
*   **Hardcoded Simulation:** No actual WMI queries for this data.

## 4. Acceptance Criteria
*   [ ] The application launches and displays "NVIDIA GeForce GTX 1650" in the appropriate UI location.
*   [ ] The VRAM is displayed as "4096 MB" (or authentic string format).
*   [ ] The `SystemInfoService` allows for changing these strings (even if no UI exists to edit them yet).
*   [ ] Architecture check passes: No code-behind logic used.
