# PROJECT_RULES: NVIDIA Control Panel Clone

> [!IMPORTANT]
> **READ CAREFULLY**: These rules are mandatory for all AI Agents and LLMs working on this codebase.

## 1. Project Context & "The Spoof"
*   **Goal**: This is a **simulated** environment. We are building a "fake" NVIDIA Control Panel.
*   **Reality Check**: The machine running this code likely DOES NOT have the hardware we claim it does (GTX 1650).
*   **Agent Behavior**: maintain the illusion.
    *   **DO NOT** write code that queries real hardware (WMI/DirectX) unless strictly for "passthrough" features.
    *   **DO** prefer `SystemInfoService` to return hardcoded/configurable "fake" values.

## 2. Technical Mandates (MVVM)
*   **Zero Code-Behind Policy**: `MainWindow.xaml.cs` must ONLY contain `InitializeComponent` and `DataContext` assignment.
*   **Services First**: Logic goes in Services. State goes in ViewModels.
*   **Dependency Injection**: Manually inject services via constructors.

## 3. Quality Assurance (The "Typescript-like" Standard)
We enforce code quality strictly, similar to `eslint` + `prettier` + `jest`.

### The "Golden Logic"
1.  **Format**: `scripts/format.ps1` (Fixes style, spacing, indentation).
2.  **Verify**: `scripts/verify.ps1` (Runs Strict Build + Tests).

### CI/CD & Hooks
*   A **Pre-Commit Hook** is installed to run `verify.ps1` automatically.
*   **NEVER** bypass this hook (`--no-verify`) unless explicitly authorized. (Use the `run_command` tool to run the verify script manually if the hook fails to understand why).

### Compiler Warnings
*   **TreatWarningsAsErrors** is **ON**.
*   Do not suppress warnings. Fix the underlying code.
*   **StyleCop** is active. Follow C# standard naming conventions (`_privateField`, `PublicProperty`).

## 4. File Structure Authority
*   `src/NvidiaControlPanel/Views`: UI (XAML)
*   `src/NvidiaControlPanel/ViewModels`: Logic (C#)
*   `src/NvidiaControlPanel/Services`: Data/System (C#)
*   `src/NvidiaControlPanel/Models`: POCOs (C#)

**Violation of these rules results in broken features and unmaintainable code.**

## 5. Design System & Theming
The application must adhere to the specific NVIDIA-like color palette defined below. Reuse these resources universally.

### Color Palette
| Name | Hex | XAML Resource Key | Usage |
| :--- | :--- | :--- | :--- |
| **NvidiaGreen** | `#76b900` | `NvidiaGreenBrush` | Primary Accents, Active States, Logo |
| **NvidiaGreenAlt** | `#6ab900` | `NvidiaGreenAltBrush` | Secondary Accents, Gradient Start |
| **NvidiaDarkGrey** | `#333333` | `NvidiaDarkGreyBrush` | Sidebar Background, Headers |
| **NvidiaBlack** | `#000000` | `NvidiaBlackBrush` | Window Background (High Contrast) |
| **NvidiaWhite** | `#ffffff` | `NvidiaWhiteBrush` | Primary Text, Content Background |

### Implementation Rules
- **NEVER** hardcode hex values in XAML views. Use `StaticResource` (e.g., `{StaticResource NvidiaGreenBrush}`).
- Define all colors in `App.xaml` as `SolidColorBrush`.
- Maintain correct contrast ratios (White text on Dark Grey/Green).
