# Technology Stack

## Core Technologies
*   **Language:** C# (C-Sharp) - The primary language for Windows application development.
*   **Framework:** .NET 10.0 (Windows) - The latest version of the Microsoft development platform.
*   **UI Framework:** WPF (Windows Presentation Foundation) - Used for building high-fidelity Windows desktop applications with modern graphics capabilities.

## Architecture & Patterns
*   **Pattern:** MVVM (Model-View-ViewModel) - A standard industry pattern that keeps the user interface (View) separate from the logic (ViewModel), making the app easier to maintain and test.
*   **Dependency Injection:** Interface-based services (e.g., `ISystemInfoService`) - This allows the app to swap between "real" system data and "simulated" data easily.
*   **Configuration Management:** `SimulationService` loads static hardware definitions from `config/gpu_config.json`, enabling external control of the spoofed identity.
*   **System Integration:** `RegistrySpoofService` and `ContextMenuService` provide on-demand UAC elevation to manage system-level integration (GPU reporting and desktop entry), ensuring external Windows tools and shell interactions report the simulated values.
*   **UX Simulation:** `FlickerService`, `ConfirmationService`, and `TrayIconService` replicate hardware-level behaviors and OS-level presence (screen blackouts, confirmation dialogs, and persistent tray icons).
*   **Visual Fidelity:** Dynamic XAML scaling and custom value converters (e.g., `DoubleToDurationConverter`) simulate hardware rendering constraints in the 3D preview without impacting real-time performance.
*   **Defensive Orchestration:** Multi-process execution via `ProcessStartInfo` handles on-demand UAC elevation for "NVIDIA Web Helper" simulations, ensuring that update attempts appear as legitimate system actions.

## Quality & Standards
*   **Static Analysis:** 
    *   **StyleCop:** Enforces strict code formatting rules to keep the project clean.
    *   **NetAnalyzers:** Automatically checks for potential bugs or security issues during development.
*   **Warning Policy:** "Treat Warnings as Errors" is enabled, ensuring the code remains at the highest quality.

## Project Structure
*   **NvidiaControlPanel.csproj:** The main project file containing all configuration and dependencies.
*   **NvidiaControlPanel.Tests:** A dedicated project for verifying that the logic works as expected.
