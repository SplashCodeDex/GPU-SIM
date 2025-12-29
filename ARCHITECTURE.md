# Architecture & Contribution Rules

## 1. Architecture Overview: MVVM
We strictly follow the **Model-View-ViewModel (MVVM)** pattern to ensure separation of concerns.

### **Views** (`src/NvidiaControlPanel/Views`)
*   **Responsibility**: Display the UI.
*   **Rule**: **Zero Logic in Code-Behind**. The `.xaml.cs` file should only contain `InitializeComponent()`.
*   **Interaction**: All user interactions (Clicks, Toggles) must be bound to **Commands** in the ViewModel.

### **ViewModels** (`src/NvidiaControlPanel/ViewModels`)
*   **Responsibility**: Handle presentation logic, hold state, and mediate between View and Services.
*   **Base Class**: All ViewModels must inherit from `ViewModelBase`.
*   **Properties**: Use `SetProperty()` to ensure `INotifyPropertyChanged` is fired.

### **Services** (`src/NvidiaControlPanel/Services`)
*   **Responsibility**: Encapsulate system logic (Registry, Files, Hardware Info).
*   **Rule**: Always define an Interface (e.g., `IRegistryService`) used for Dependency Injection.
*   **Reason**: This allows us to mock system calls during testing or simulation.

## 2. Project Structure
```text
src/
├── Models/       # Data structures (POCOs)
├── Services/     # Interfaces and Implementations for system logic
├── ViewModels/   # Logic for Views
│   └── Core/     # Helpers like RelayCommand, ViewModelBase
└── Views/        # XAML files
```

## 3. Deployment Rules
*   **Self-Contained**: The final build must be a single `.exe` file.
*   **No Dependencies**: Do not rely on external DLLs that aren't packed.
