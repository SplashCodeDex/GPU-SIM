# NVIDIA Control Panel Clone

A high-fidelity clone of the NVIDIA Control Panel application, designed for simulation and testing purposes.

## 🚀 Getting Started

### Prerequisites
*   **.NET 10 SDK** (or newer)
*   Windows OS (for WPF support)

### Building the Project
Open the solution in Visual Studio or run via CLI:
```bash
dotnet build src/NvidiaControlPanel/NvidiaControlPanel.csproj
```

### Running
```bash
dotnet run --project src/NvidiaControlPanel/NvidiaControlPanel.csproj
```

## 📐 Architecture
This project adheres to strict **Clean Architecture** principles using the **MVVM** pattern.
Please read [ARCHITECTURE.md](ARCHITECTURE.md) before contributing to ensure you follow the project rules.

## 🤝 Contributing
*   **Views**: UI only (XAML). No code-behind logic.
*   **ViewModels**: Logic and State.
*   **Services**: System interactions.

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed guidelines.
