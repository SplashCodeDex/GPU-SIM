---
description: Standard procedure for adding a new feature or page to the Control Panel.
---

# Workflow: Feature Implementation

Follow this strictly to ensure MVVM compliance.

1.  **Define the Requirement**
    *   Identify what data is needed (e.g., "Fan Speed").
    *   Identify where it goes in the UI (e.g., "Performance" category).

2.  **Service Layer (The Data)**
    *   Check `SystemInfoService` (or relevant service).
    *   Add method/property to Interface (e.g., `IFanControlService.GetFanSpeed()`).
    *   Implement fake static data in the concrete Service class.

3.  **ViewModel Layer (The Logic)**
    *   Create or Update a ViewModel (e.g., `PerformanceViewModel`).
    *   Inject the Service.
    *   Expose properties (e.g., `public string FanSpeed { get; }`).
    *   Create Commands for any buttons.

4.  **View Layer (The UI)**
    *   Create/Update the XAML.
    *   **Bind** elements to the ViewModel Properties.
    *   **Bind** buttons to Commands.
    *   **DO NOT** add `Click` handlers.

5.  **Integration**
    *   Register the new ViewModel/View mapping if using a DataTemplate, or update `MainWindow` to display it.

6.  **Verification**
    *   Run `dotnet build`.
    *   Run app and visually inspect.
