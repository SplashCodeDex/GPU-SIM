using System.Collections.Generic;
using System.Collections.ObjectModel;
using NvidiaControlPanel.Models;
using NvidiaControlPanel.Services;
using NvidiaControlPanel.ViewModels.Core;

namespace NvidiaControlPanel.ViewModels
{
    /// <summary>
    /// ViewModel for the 'Manage 3D Settings' page.
    /// </summary>
    public class Manage3DSettingsViewModel : ViewModelBase
    {
        private readonly ISettingsService _settingsService;
        private readonly GpuInformation _gpuInformation;

        /// <summary>
        /// Initializes a new instance of the <see cref="Manage3DSettingsViewModel"/> class.
        /// </summary>
        public Manage3DSettingsViewModel()
            : this(new JsonSettingsService(), new GpuInformation { GpuName = "NVIDIA GeForce GTX 1650 (Design)" })
        {
        }

        /// <summary>
        /// Initializes a new instance of the <see cref="Manage3DSettingsViewModel"/> class with dependencies.
        /// </summary>
        /// <param name="settingsService">The settings service.</param>
        /// <param name="gpuInformation">The GPU information.</param>
        public Manage3DSettingsViewModel(ISettingsService settingsService, GpuInformation gpuInformation)
        {
            this._settingsService = settingsService;
            this._gpuInformation = gpuInformation;
            this.Settings = new ObservableCollection<FeatureSetting>();
            this.RestoreDefaultsCommand = new RelayCommand(this.ExecuteRestoreDefaults);
            this.ApplyCommand = new RelayCommand(this.ExecuteApply);

            this.LoadSettings();
        }

        /// <summary>
        /// Gets the collection of 3D settings.
        /// </summary>
        public ObservableCollection<FeatureSetting> Settings { get; }

        /// <summary>
        /// Gets the collection of available programs.
        /// </summary>
        public ObservableCollection<string> Programs { get; } = new ObservableCollection<string>();

        /// <summary>
        /// Gets or sets the selected program.
        /// </summary>
        public string? SelectedProgram { get; set; }

        /// <summary>
        /// Gets the command to restore default settings.
        /// </summary>
        public System.Windows.Input.ICommand RestoreDefaultsCommand { get; }

        /// <summary>
        /// Gets the command to save and apply settings.
        /// </summary>
        public System.Windows.Input.ICommand ApplyCommand { get; }

        private Collection<FeatureSetting> GetDefaultSettings()
        {
            var defaults = new Collection<FeatureSetting>
            {
                new FeatureSetting { Name = "Image Sharpening", Value = "Off", DefaultValue = "Off", Options = { "Off", "On" } },
                new FeatureSetting { Name = "Ambient Occlusion", Value = "Performance", DefaultValue = "Performance", Options = { "Off", "Performance", "Quality" } },
                new FeatureSetting { Name = "Anisotropic filtering", Value = "Application-controlled", DefaultValue = "Application-controlled", Options = { "Application-controlled", "Off", "2x", "4x", "8x", "16x" } },
                new FeatureSetting { Name = "Antialiasing - FXAA", Value = "Off", DefaultValue = "Off", Options = { "Off", "On" } },
                new FeatureSetting { Name = "Antialiasing - Gamma correction", Value = "On", DefaultValue = "On", Options = { "Off", "On" } },
                new FeatureSetting { Name = "Antialiasing - Mode", Value = "Application-controlled", DefaultValue = "Application-controlled", Options = { "Application-controlled", "Off", "Enhance the application setting", "Override any application setting" } },
                new FeatureSetting { Name = "Background Application Max Frame Rate", Value = "Off", DefaultValue = "Off", Options = { "Off", "On" } },
                new FeatureSetting { Name = "CUDA - GPUs", Value = "All", DefaultValue = "All", Options = { "All", "None" } },
                new FeatureSetting { Name = "DSR - Factors", Value = "Off", DefaultValue = "Off", Options = { "Off", "1.20x", "1.50x", "2.00x", "4.00x" } },
                new FeatureSetting { Name = "Low Latency Mode", Value = "Off", DefaultValue = "Off", Options = { "Off", "On", "Ultra" } },
                new FeatureSetting { Name = "Max Frame Rate", Value = "Off", DefaultValue = "Off", Options = { "Off", "On" } },
                new FeatureSetting { Name = "Monitor Technology", Value = "G-SYNC Compatible", DefaultValue = "G-SYNC Compatible", Options = { "Fixed Refresh", "G-SYNC Compatible" } },
                new FeatureSetting { Name = "Multi-Frame Sampled AA (MFAA)", Value = "Off", DefaultValue = "Off", Options = { "Off", "On" } },
                new FeatureSetting { Name = "OpenGL rendering GPU", Value = "Auto-select", DefaultValue = "Auto-select", Options = { "Auto-select", this._gpuInformation?.GpuName ?? "NVIDIA GPU" } },
                new FeatureSetting { Name = "Power management mode", Value = "Normal", DefaultValue = "Normal", Options = { "Normal", "Prefer maximum performance" } },
                new FeatureSetting { Name = "Preferred refresh rate", Value = "Highest available", DefaultValue = "Highest available", Options = { "Application-controlled", "Highest available" } },
                new FeatureSetting { Name = "Shader Cache Size", Value = "Driver Default", DefaultValue = "Driver Default", Options = { "Driver Default", "Disabled", "Unlimited", "10 GB", "100 GB" } },
                new FeatureSetting { Name = "Texture filtering - Anisotropic sample optimization", Value = "Off", DefaultValue = "Off", Options = { "Off", "On" } },
                new FeatureSetting { Name = "Texture filtering - Negative LOD bias", Value = "Allow", DefaultValue = "Allow", Options = { "Allow", "Clamp" } },
                new FeatureSetting { Name = "Texture filtering - Quality", Value = "Quality", DefaultValue = "Quality", Options = { "High Quality", "Quality", "Performance", "High Performance" } },
                new FeatureSetting { Name = "Texture filtering - Trilinear optimization", Value = "On", DefaultValue = "On", Options = { "Off", "On" } },
                new FeatureSetting { Name = "Threaded optimization", Value = "Auto", DefaultValue = "Auto", Options = { "Auto", "Off", "On" } },
                new FeatureSetting { Name = "Triple buffering", Value = "Off", DefaultValue = "Off", Options = { "Off", "On" } },
                new FeatureSetting { Name = "Vertical sync", Value = "Use the 3D application setting", DefaultValue = "Use the 3D application setting", Options = { "Use the 3D application setting", "Off", "On", "Adaptive", "Adaptive (half refresh rate)", "Fast" } },
                new FeatureSetting { Name = "Virtual Reality pre-rendered frames", Value = "1", DefaultValue = "1", Options = { "1", "2", "3", "4" } },
            };
            return defaults;
        }

        private void LoadSettings()
        {
            // Start with defaults
            var settings = this.GetDefaultSettings();

            // Try load saved
            var loaded = this._settingsService.Load3DSettings();
            if (loaded != null && loaded.Count > 0)
            {
                foreach (var loadedSetting in loaded)
                {
                    // Find matching default setting
                    var existing = System.Linq.Enumerable.FirstOrDefault(settings, s => s.Name == loadedSetting.Name);
                    if (existing != null)
                    {
                        existing.Value = loadedSetting.Value;
                    }
                }
            }

            this.Settings.Clear();
            foreach (var setting in settings)
            {
                this.Settings.Add(setting);
            }

            // Load Programs
            var programs = this._settingsService.GetAvailablePrograms();
            foreach (var prog in programs)
            {
                this.Programs.Add(prog);
            }

            if (this.Programs.Count > 0)
            {
                this.SelectedProgram = this.Programs[0];
            }
        }

        private void ExecuteApply(object? obj)
        {
            this._settingsService.Save3DSettings(this.Settings);
        }

        private void ExecuteRestoreDefaults(object? obj)
        {
            // Reset all to default values
            foreach (var setting in this.Settings)
            {
                setting.Value = setting.DefaultValue;
            }

            // Save immediately or let user Click Apply? Real NCP usually applies Restore immediately or updates UI.
            // For now just update UI.
            // Ideally we might want to refresh the view or force property changed if needed, but binding should handle it.
        }
    }
}
