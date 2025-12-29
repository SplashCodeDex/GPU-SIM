using System.Windows;
using System.Windows.Input;
using NvidiaControlPanel.Services;
using NvidiaControlPanel.ViewModels.Core;

namespace NvidiaControlPanel.ViewModels
{
    /// <summary>
    /// The Main ViewModel for the application.
    /// </summary>
    public class MainViewModel : ViewModelBase
    {
        private readonly IRegistryService _registryService;
        private readonly ISystemInfoService _systemInfoService;
        private object _currentView = new Manage3DSettingsViewModel();
        private string _currentPath = "3D Settings > Manage 3D settings";
        private bool _isContextMenuEnabled;

        /// <summary>
        /// Initializes a new instance of the <see cref="MainViewModel"/> class.
        /// </summary>
        public MainViewModel()
            : this(new RegistryService(), new SystemInfoService())
        {
            // Default constructor for design-time data if needed
        }

        /// <summary>
        /// Initializes a new instance of the <see cref="MainViewModel"/> class with dependencies.
        /// </summary>
        /// <param name="registryService">The registry service.</param>
        /// <param name="systemInfoService">The system info service.</param>
        public MainViewModel(IRegistryService registryService, ISystemInfoService systemInfoService)
        {
            this._registryService = registryService;
            this._systemInfoService = systemInfoService;

            // Initialize Command
            this.ExitCommand = new RelayCommand(this.ExecuteExit);
            this.ShowSystemInfoCommand = new RelayCommand(this.ExecuteShowSystemInfo);
            this.ToggleContextMenuCommand = new RelayCommand(this.ExecuteToggleContextMenu);
            this.NavigateCommand = new RelayCommand(this.ExecuteNavigate);

            // Load initial state
            this.IsContextMenuEnabled = this._registryService.IsContextMenuEnabled();

            // Default View
            this.CurrentView = new Manage3DSettingsViewModel();
        }

        /// <summary>
        /// Gets or sets the currently displayed view model.
        /// </summary>
        public object CurrentView
        {
            get => this._currentView;
            set => this.SetProperty(ref this._currentView, value);
        }

        /// <summary>
        /// Gets or sets the current navigation path.
        /// </summary>
        public string CurrentPath
        {
            get => this._currentPath;
            set => this.SetProperty(ref this._currentPath, value);
        }

        /// <summary>
        /// Gets or sets a value indicating whether the Context Menu entry is enabled.
        /// </summary>
        public bool IsContextMenuEnabled
        {
            get => this._isContextMenuEnabled;
            set
            {
                if (this.SetProperty(ref this._isContextMenuEnabled, value))
                {
                    // Logic is handled in the Command, but state is reflected here
                }
            }
        }

        /// <summary>
        /// Gets the command to exit the application.
        /// </summary>
        public ICommand ExitCommand { get; }

        /// <summary>
        /// Gets the command to show system information.
        /// </summary>
        public ICommand ShowSystemInfoCommand { get; }

        /// <summary>
        /// Gets the command to toggle the context menu.
        /// </summary>
        public ICommand ToggleContextMenuCommand { get; }

        /// <summary>
        /// Gets the command to navigate to a specific view.
        /// </summary>
        public ICommand NavigateCommand { get; }

        private void ExecuteExit(object? obj)
        {
            Application.Current.Shutdown();
        }

        private void ExecuteNavigate(object? obj)
        {
            if (obj is string viewName)
            {
                switch (viewName)
                {
                    case "Manage3DSettings":
                        this.CurrentView = new Manage3DSettingsViewModel();
                        this.CurrentPath = "3D Settings > Manage 3D settings";
                        break;
                    case "ChangeResolution":
                        this.CurrentView = new DisplayResolutionViewModel();
                        this.CurrentPath = "Display > Change resolution";
                        break;
                    default:
                        // Placeholder for other pages
                        break;
                }
            }
        }

        private void ExecuteShowSystemInfo(object? obj)
        {
            var info = this._systemInfoService.GetGpuInformation();
            string message = $"NVIDIA System Information\n\n" +
                             $"GPU: {info.GpuName}\n" +
                             $"Driver Version: {info.DriverVersion}\n" +
                             $"Memory: {info.VideoMemory}\n\n";

            MessageBox.Show(message, "System Information");
        }

        private void ExecuteToggleContextMenu(object? obj)
        {
            if (this.IsContextMenuEnabled)
            {
                this._registryService.EnableContextMenu();
            }
            else
            {
                this._registryService.DisableContextMenu();
            }
        }
    }
}
