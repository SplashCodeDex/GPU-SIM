# Initial Concept
A high-fidelity clone of the NVIDIA Control Panel application, designed for simulation and testing purposes.

# Product Guide: NVIDIA GPU Simulator & Control Panel

## 1. Vision
To create a sophisticated simulation environment that mimics the presence of dedicated NVIDIA graphics hardware on a Windows PC. The system serves as a "prank" or demonstration tool, capable of fooling standard system verification tools (Task Manager, dxdiag, Settings) and providing a fully interactive, authentic replica of the NVIDIA Control Panel.

## 2. Target Audience
*   **Primary User:** The project creator (for demonstrating the "fake" GPU to friends).
*   **Secondary Users:** Enthusiasts interested in hardware spoofing or UI replication.

## 3. Core Goals
*   **System-Wide Deception:** The simulated GPU must be detectable and display correct "spoofed" specifications (Model, VRAM) in:
    *   Windows Task Manager
    *   DirectX Diagnostic Tool (dxdiag)
    *   Windows Settings > System > Display
*   **Authentic Control Panel:** The `NvidiaControlPanel` app must be indistinguishable from the real application in look and feel.
*   **Configuration:** Users can select different GPU profiles (e.g., GTX 1650, RTX 3060) to "install" on the system.
*   **Seamless Deployment:** Automated GitHub Actions pipeline to build and release a standalone, portable `.exe` for quick deployment.

## 4. Key Features
*   **GPU Profile Manager:** Configure the "virtual" GPU's details (Name, VRAM size, Driver Version, Bus Support, BIOS Version, DirectX Support, Device/Vendor IDs).
*   **System Hooking/Spoofing:** (Future/Advanced) Mechanisms to inject these values into Windows reporting tools.
*   **High-Fidelity UI:** A WPF-based interface that strictly adheres to the visual style of the legacy NVIDIA Control Panel.
*   **One-Click "Installation":** A setup routine that registers the spoofed values and places the Control Panel app appropriately.
*   **Static Configuration:** Loads hardware definitions from `config/gpu_config.json` for easy manual spoofing.

## 5. User Flow
1.  **Build:** Developer pushes a tag to GitHub.
2.  **Release:** GitHub Action builds the standalone `NvidiaControlPanel.exe`.
3.  **Deploy:** User downloads and runs the executable on the target machine.
4.  **Configure:** User selects a target GPU profile (e.g., "GTX 1650 4GB").
5.  **Simulate:** The app applies changes to system registries/hooks.
6.  **Verify:** The "friend" checks Task Manager/dxdiag and sees the fake GPU, then opens the Control Panel to verify settings.