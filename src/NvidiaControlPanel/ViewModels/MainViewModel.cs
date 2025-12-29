using System.Threading.Tasks;
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
        private readonly IContextMenuService _contextMenuService;
        private readonly ISystemInfoService _systemInfoService;
        private readonly ITrayIconService _trayIconService;
        private readonly IAutoStartService _autoStartService;
        private readonly INavigationService _navigationService;
        private object _currentView;
        private string _currentPath = "NVIDIA Control Panel";
        private string _statusBarText = string.Empty;
        private bool _isContextMenuEnabled;
        private bool _isTrayIconVisible = true;
        private bool _isAutoStartEnabled;
        private NvidiaControlPanel.Models.GpuInformation? _gpuInformation;

        /// <summary>
        /// Initializes a new instance of the <see cref="MainViewModel"/> class.
        /// </summary>
        [System.Diagnostics.CodeAnalysis.SuppressMessage("Reliability", "CA2000:Dispose objects before losing scope", Justification = "Service lifecycle is managed by the application.")]
        public MainViewModel()
            : this(new ContextMenuService(), new SystemInfoService(), new TrayIconService(), new AutoStartService(), new NavigationService())
        {
            // Default constructor for design-time data if needed
        }

        /// <summary>
        /// Initializes a new instance of the <see cref="MainViewModel"/> class with dependencies.
        /// </summary>
        /// <param name="contextMenuService">The context menu service.</param>
        /// <param name="systemInfoService">The system info service.</param>
        /// <param name="trayIconService">The tray icon service.</param>
        /// <param name="autoStartService">The auto-start service.</param>
        /// <param name="navigationService">The navigation service.</param>
        public MainViewModel(
            IContextMenuService contextMenuService,
            ISystemInfoService systemInfoService,
            ITrayIconService trayIconService,
            IAutoStartService autoStartService,
            INavigationService navigationService)
        {
            this._contextMenuService = contextMenuService;
            this._systemInfoService = systemInfoService;
            this._trayIconService = trayIconService;
            this._autoStartService = autoStartService;
            this._navigationService = navigationService;

            // Initialize Command
            this.ExitCommand = new RelayCommand(this.ExecuteExit);
            this.ShowSystemInfoCommand = new RelayCommand(this.ExecuteShowSystemInfo);
            this.ToggleContextMenuCommand = new RelayCommand(this.ExecuteToggleContextMenu);
            this.ToggleTrayIconCommand = new RelayCommand(this.ExecuteToggleTrayIcon);
            this.ToggleAutoStartCommand = new RelayCommand(this.ExecuteToggleAutoStart);
            this.NavigateCommand = new RelayCommand(this.ExecuteNavigate);
            this.BackCommand = new RelayCommand(this.ExecuteBack, _ => this._navigationService.CanGoBack);
            this.ForwardCommand = new RelayCommand(this.ExecuteForward, _ => this._navigationService.CanGoForward);

            // Load initial state
            this.IsContextMenuEnabled = this._contextMenuService.IsEnabled();
            this.IsAutoStartEnabled = this._autoStartService.IsEnabled();

            // Default valid value to satisfy non-nullable requirement
            this._currentView = new PlaceholderViewModel("Loading...");

            // Initialize Async
            _ = this.InitializeAsync();
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
        /// Gets or sets a value indicating whether auto-start is enabled.
        /// </summary>
        public bool IsAutoStartEnabled
        {
            get => this._isAutoStartEnabled;
            set
            {
                if (this.SetProperty(ref this._isAutoStartEnabled, value))
                {
                    // Logic is handled in the Command
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
        /// Gets the command to toggle auto-start.
        /// </summary>
        public ICommand ToggleAutoStartCommand { get; }

        /// <summary>
        /// Gets or sets a value indicating whether the tray icon is visible.
        /// </summary>
        public bool IsTrayIconVisible
        {
            get => this._isTrayIconVisible;
            set => this.SetProperty(ref this._isTrayIconVisible, value);
        }

        /// <summary>
        /// Gets the command to navigate to a specific view.
        /// </summary>
        public ICommand NavigateCommand { get; }

        /// <summary>
        /// Gets the command to navigate back in history.
        /// </summary>
        public ICommand BackCommand { get; }

        /// <summary>
        /// Gets the command to navigate forward in history.
        /// </summary>
        public ICommand ForwardCommand { get; }

        private async Task InitializeAsync()
        {
            try
            {
                var info = await this._systemInfoService.GetGpuInformationAsync().ConfigureAwait(true);
                this._gpuInformation = info;
                this.StatusBarText = $"System Information: {info.GpuName}";
                this.IsTrayIconVisible = info.IsTrayIconVisible;
                this._trayIconService.SetVisibility(this.IsTrayIconVisible);

                // Default View
                this.CurrentView = new HomeViewModel(info);
            }
            catch
            {
                this.StatusBarText = "Failed to load system information.";
            }
        }

        private void ExecuteExit(object? obj)
        {
            Application.Current.Shutdown();
        }

        private void ExecuteNavigate(object? obj)
        {
            if (obj is string viewName)
            {
                this._navigationService.RecordNavigation(viewName);
                this.NavigateToView(viewName);
                CommandManager.InvalidateRequerySuggested();
            }
        }

        private void ExecuteBack(object? obj)
        {
            var viewName = this._navigationService.GoBack();
            if (viewName != null)
            {
                this.NavigateToView(viewName);
                CommandManager.InvalidateRequerySuggested();
            }
        }

        private void ExecuteForward(object? obj)
        {
            var viewName = this._navigationService.GoForward();
            if (viewName != null)
            {
                this.NavigateToView(viewName);
                CommandManager.InvalidateRequerySuggested();
            }
        }

        private void NavigateToView(string viewName)
        {
            switch (viewName)
                {
                    case "Home":
                        if (this._gpuInformation != null)
                        {
                            this.CurrentView = new HomeViewModel(this._gpuInformation);
                        }
                        else
                        {
                            this.CurrentView = new PlaceholderViewModel("Home");
                        }

                        this.CurrentPath = "NVIDIA Control Panel";
                        break;
                    case "Manage3DSettings":
                        if (this._gpuInformation != null)
                        {
                            this.CurrentView = new Manage3DSettingsViewModel(new JsonSettingsService(), this._gpuInformation);
                        }
                        else
                        {
                            // Output a default if not yet loaded
                            this.CurrentView = new Manage3DSettingsViewModel();
                        }

                        this.CurrentPath = "3D Settings > Manage 3D settings";
                        break;
                    case "ChangeResolution":
                        this.CurrentView = new DisplayResolutionViewModel(
                            new MockDisplayService(),
                            this._systemInfoService is SystemInfoService s ? new SimulationService() : new SimulationService(), // fallback
                            new FlickerService(),
                            new ConfirmationService());
                        this.CurrentPath = "Display > Change resolution";
                        break;
                    case "AdjustImageSettings":
                        this.CurrentView = new AdjustImageSettingsViewModel();
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

        private async void ExecuteShowSystemInfo(object? obj)
        {
            var info = await this._systemInfoService.GetGpuInformationAsync().ConfigureAwait(true);
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
                this._contextMenuService.Enable();
            }
            else
            {
                this._contextMenuService.Disable();
            }
        }

        private void ExecuteToggleAutoStart(object? obj)
        {
            if (this.IsAutoStartEnabled)
            {
                this._autoStartService.Enable();
            }
            else
            {
                this._autoStartService.Disable();
            }
        }

        private void ExecuteToggleTrayIcon(object? obj)
        {
            this.IsTrayIconVisible = !this.IsTrayIconVisible;
            this._trayIconService.SetVisibility(this.IsTrayIconVisible);
        }
    }
}
