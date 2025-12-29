# Product Guidelines

## 1. Visual Identity
*   **Style Strategy:** "Enhanced Legacy." While the layout must remain instantly recognizable as the classic NVIDIA Control Panel to maintain the ruse, we will subtly elevate the quality.
    *   **Authenticity First:** The core structure (tree view on left, settings pane on right), icons, and color palette (NVIDIA Green #76B900) must be exact replicas.
    *   **Modern Polish:** Use modern WPF rendering capabilities to eliminate the "clunky" feel of the original Forms-based app. Fonts should be crisp (Segoe UI), and elements should align perfectly.
    *   **Subtle Modernization:** Introduce gentle, non-intrusive effects like slight drop shadows on active windows or smoother anti-aliasing on the 3D preview logo to give a "premium" subconscious feel.

## 2. Voice & Tone
*   **Approach:** Ultra-Realistic Mimicry.
*   **Language:** The application must speak exactly like a hardware driver. Use formal, technical, and declarative language.
    *   *Correct:* "The display configuration has changed."
    *   *Incorrect:* "Your screen settings are updated!"
*   **Error Handling:** Replicate authentic error codes and help text. If a user tries to access a feature that isn't fully simulated, the error message should blame a "Driver Compatibility" issue or "Pending System Restart" rather than revealing the simulation.

## 3. Interaction & UX
*   **"Selling the Lie":** The simulation relies on behavioral cues, not just static pixels.
    *   **Screen Flicker:** When changing display settings (Resolution, Refresh Rate), the app MUST simulate a "mode switch" by briefly flickering the screen or showing a black screen overlay. This physical feedback is critical for convincing the user that hardware is being addressed.
    *   **Artificial Latency:** "Apply" buttons should not be instant. Introduce a calculated delay (0.5s - 1.5s) with a loading cursor to mimic the time a real GPU takes to reconfigure buffers.
    *   **Smooth Transitions:** Use high-quality, high-refresh-rate animations for menu expansions and the 3D spinning logo preview to contrast with the "clunky" original, reinforcing the "this PC is powerful" narrative.

## 4. Feature Implementation & Constraints
*   **The "Driver Update" Defense:**
    *   We acknowledge that physical hardware limits (e.g., maximum screen resolution/refresh rate) cannot be physically bypassed.
    *   **Strategy:** Options that exceed physical capabilities (e.g., 4K on a 1080p screen) should be visible but **disabled (grayed out)**.
    *   **Justification:** A tooltip or message should indicate: *"This setting requires a driver update"* or *"Display cable bandwidth exceeded."* This deflects scrutiny away from the fake GPU and towards plausible technical issues.
*   **Verification Strategy:**
    *   Success is defined by the **Observer's Belief**.
    *   If a setting cannot be hooked into Windows (Task Manager), the app itself must act as the source of truth, displaying the "spoofed" values with high confidence.
