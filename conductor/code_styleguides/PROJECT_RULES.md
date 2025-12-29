# PROJECT_RULES: NVIDIA Control Panel Clone

> [!IMPORTANT]
> **READ CAREFULLY**: These rules are mandatory for all AI Agents and LLMs working on this codebase.

## 1. Project Context & "The Spoof"
*   **Goal**: This is a **simulated** environment. We are building a "fake" NVIDIA Control Panel.
*   **Reality Check**: The machine running this code likely DOES NOT have the hardware we claim it does (GTX 1650).
*   **Agent Behavior**: maintain the illusion.
    *   **DO NOT** write code that queries real hardware (WMI/DirectX) unless strictly for "passthrough" features.
    *   **DO** prefer `SystemInfoService` to return hardcoded/configurable "fake" values.
    *   **DO NOT** "fix" the hardcoded GPU strings by replacing them with real hardware queries. That defeats the purpose.

## 2. Technical Mandates (MVVM)
*   **Zero Code-Behind Policy**:
    *   Stop. Look at `MainWindow.xaml.cs`.
    *   Does it contain anything other than `InitializeComponent()` or `DataContext = ...`?
    *   If **YES**: You have failed. Refactor it to a ViewModel Command immediately.
*   **Services First**:
    *   Never instantiate logic directly in a ViewModel.
    *   Create an Interface -> Implement Service -> Inject into ViewModel.

## 3. Interaction Protocols
*   **Run Verification**: After *every* code change, you must run the `verification_routine` workflow.
*   **No "Blind" Edits**: Do not assume file state. Read it, Plan it, Edit it, Verify it.

## 4. File Structure Authority
*   `src/NvidiaControlPanel/Views`: UI (XAML)
*   `src/NvidiaControlPanel/ViewModels`: Logic (C#)
*   `src/NvidiaControlPanel/Services`: Data/System (C#)
*   `src/NvidiaControlPanel/Models`: POCOs (C#)

**Violation of these rules results in broken features and unmaintainable code.**
