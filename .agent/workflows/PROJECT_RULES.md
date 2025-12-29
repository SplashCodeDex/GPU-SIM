# PROJECT_RULES: NVIDIA Control Panel Clone (V2.0)

> [!IMPORTANT]
> **READ CAREFULLY**: These rules are **MANDATORY** for all AI Agents and LLMs. Strict adherence is required to maintain the "Reference Quality" of this simulation.

## 1. The "Deep Spoof" Protocol
*   **Goal**: Create an indistinguishable clone of the NVIDIA Control Panel.
*   **Simulation vs. Reality**:
    *   **NEVER** query real hardware (WMI, DirectX, Registry) for GPU stats. The reference machine may not have an NVIDIA GPU.
    *   **ALWAYS** use the `SimulationConfig` service. Hardware details (GPU Name, RAM, Driver Version) must be loaded from `simulation_config.json`.
    *   **Passthrough**: Application-level settings (e.g., "Developer Mode") can be real, but hardware-level strings must be spoofed.

## 2. Visual Design System (Strict)
*   **Aesthetic Goal**: "Industrial, Technical, Premium".
*   **Icons**:
    *   **BANNED**: Text-based icons (emojis), raster images for UI icons.
    *   **REQUIRED**: `MahApps.Metro.IconPacks.Material`. Use vector icons for all buttons, menus, and tree items.
*   **Typography**:
    *   Primary Font: `Segoe UI` (Standard Windows).
    *   Sizes: `12px` (Status), `14px` (Body), `16px` (Headers).
*   **Palette** (Defined in `App.xaml`):
    *   `NvidiaGreen`: `#76b900` (Brand dominance)
    *   `Background`: `#FFFFFF` (Content), `#F0F0F0` (Chrome)
    *   `Text`: `#333333` (Primary), `#666666` (Secondary)

## 3. Architecture & MVVM Mandates
*   **Zero Code-Behind**: `*.xaml.cs` files must contain **ONLY** `InitializeComponent()`. All logic goes to ViewModels.
*   **Service Pattern**:
    *   Logic must exist in **Services** (`ISettingsService`, `SystemInfoService`).
    *   ViewModels receive Services via **Dependency Injection** (Constructor Injection).
*   **Async/Await**: All I/O (File access, "Fake" loading delays) must be `async`. Never block the UI thread.
*   **Input Validation**: All simulated inputs must validate data types (e.g., Refresh Rate must be an integer).

## 4. Modern C# Standards (.NET 10.0)
*   **Nullable Reference Types**: `<Nullable>enable</Nullable>` is on. Handle `null` explicitly.
*   **File-Scoped Namespaces**: Use `namespace NvidiaControlPanel.Services;` instead of block-scoped.
*   **Global Usings**: Common namespaces should be global.

## 5. Workflow & Verification
*   **Pre-Commit Check**: Before finalizing any task, run `dotnet build`.
*   **Visual Verification**: UI changes must be verified via Walkthroughs (screenshots/recordings).
*   **No "Blind" Edits**: Always read the target file state before applying patches.

## 6. Testing Protocol
*   **Mandate**: All "Testable" logic (Services, Logical ViewModels) **MUST** have corresponding Unit Tests.
*   **Tooling**: Use `xUnit` in a dedicated `NvidiaControlPanel.Tests` project.
*   **Requirement**: `dotnet test` must return **PASS** before any task completion.
*   **Scope**:
    *   **Services**: Verify logic paths and error handling.
    *   **ViewModels**: Verify Command execution and Property notifications.

---
**Violation of these rules breaks the simulation and is considered a critical failure.**
