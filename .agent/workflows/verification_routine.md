---
description: Mandatory steps to verify code stability and architecture.
---

# Workflow: Verification Routine

Run this after every set of changes.

// turbo-all

1.  **Build the Project**
    ```powershell
    dotnet build src/NvidiaControlPanel/NvidiaControlPanel.csproj
    ```

2.  **Architecture Check (Manual)**
    *   Read `*.xaml.cs` files in `src/NvidiaControlPanel/Views`.
    *   **PASS**: File contains ONLY `InitializeComponent` and `DataContext`.
    *   **FAIL**: File contains logic, calculations, or `Click` handlers. -> **TRIGGER REFACTOR**.

3.  **Runtime Check** (If applicable)
    *   Run the app: `dotnet run --project src/NvidiaControlPanel/NvidiaControlPanel.csproj`
    *   Verify startup without crash.
    *   (Agent cannot see the window, but assume success if process stays alive > 2 seconds).
