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
        private object _currentView;
        private string _currentPath = "NVIDIA Control Panel";
        private string _statusBarText = string.Empty;
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
            this.ToggleTrayIconCommand = new RelayCommand(this.ExecuteToggleTrayIcon);
            this.NavigateCommand = new RelayCommand(this.ExecuteNavigate);

            // Load initial state
            this.IsContextMenuEnabled = this._registryService.IsContextMenuEnabled();

            // Set StatusBar Text
            var info = this._systemInfoService.GetGpuInformation();
            this.StatusBarText = $"System Information: {info.GpuName}";

            // Default View
            this._currentView = new HomeViewModel(info);
        }

        /// <summary>
        /// Gets or sets the text displayed in the status bar.
        /// </summary>
        public string StatusBarText
        {
            get => this._statusBarText;
            set => this.SetProperty(ref this._statusBarText, value);
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
        /// Gets the command to toggle the tray icon visibility.
        /// </summary>
        public ICommand ToggleTrayIconCommand { get; }

        /// <summary>
        /// Gets a value indicating whether the tray icon is visible.
        /// </summary>
        public bool IsTrayIconVisible { get; private set; } = true;

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
                    case "AdjustImageSettings":
                        this.CurrentView = new PlaceholderViewModel("Adjust image settings with preview");
                        this.CurrentPath = "3D Settings > Adjust image settings with preview";
                        break;
                    case "ConfigureSurroundPhysX":
                        this.CurrentView = new PlaceholderViewModel("Configure Surround, PhysX");
                        this.CurrentPath = "3D Settings > Configure Surround, PhysX";
                        break;
                    case "AdjustDesktopColor":
                        this.CurrentView = new PlaceholderViewModel("Adjust desktop color settings");
                        this.CurrentPath = "Display > Adjust desktop color settings";
                        break;
                    case "RotateDisplay":
                        this.CurrentView = new PlaceholderViewModel("Rotate display");
                        this.CurrentPath = "Display > Rotate display";
                        break;
                    case "ViewHDCPStatus":
                        this.CurrentView = new PlaceholderViewModel("View HDCP status");
                        this.CurrentPath = "Display > View HDCP status";
                        break;
                    case "SetupDigitalAudio":
                        this.CurrentView = new PlaceholderViewModel("Set up digital audio");
                        this.CurrentPath = "Display > Set up digital audio";
                        break;
                    case "AdjustDesktopSizePosition":
                        this.CurrentView = new PlaceholderViewModel("Adjust desktop size and position");
                        this.CurrentPath = "Display > Adjust desktop size and position";
                        break;
                    case "SetupMultipleDisplays":
                        this.CurrentView = new PlaceholderViewModel("Set up multiple displays");
                        this.CurrentPath = "Display > Set up multiple displays";
                        break;
                    case "AdjustVideoColor":
                        this.CurrentView = new PlaceholderViewModel("Adjust video color settings");
                        this.CurrentPath = "Video > Adjust video color settings";
                        break;
                    case "AdjustVideoImage":
                        this.CurrentView = new PlaceholderViewModel("Adjust video image settings");
                        this.CurrentPath = "Video > Adjust video image settings";
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
            var vm = new SystemInfoViewModel(info);
            var view = new Views.SystemInfoView
            {
                DataContext = vm,
                Owner = Application.Current.MainWindow,
            };

            view.ShowDialog();
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

        private void ExecuteToggleTrayIcon(object? obj)
        {
            this.IsTrayIconVisible = !this.IsTrayIconVisible;
            this.OnPropertyChanged(nameof(this.IsTrayIconVisible));
        }
    }
}
