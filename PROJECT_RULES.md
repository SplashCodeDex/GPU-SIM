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
