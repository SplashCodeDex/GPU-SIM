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

        /// <summary>
        /// Initializes a new instance of the <see cref="Manage3DSettingsViewModel"/> class.
        /// </summary>
        public Manage3DSettingsViewModel()
            : this(new JsonSettingsService())
        {
        }

        /// <summary>
        /// Initializes a new instance of the <see cref="Manage3DSettingsViewModel"/> class with dependencies.
        /// </summary>
        /// <param name="settingsService">The settings service.</param>
        public Manage3DSettingsViewModel(ISettingsService settingsService)
        {
            this._settingsService = settingsService;
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
        /// Gets the command to restore default settings.
        /// </summary>
        public System.Windows.Input.ICommand RestoreDefaultsCommand { get; }

        /// <summary>
        /// Gets the command to save and apply settings.
        /// </summary>
        public System.Windows.Input.ICommand ApplyCommand { get; }

        private static Collection<FeatureSetting> GetDefaultSettings()
        {
            return new Collection<FeatureSetting>
            {
                new FeatureSetting { Name = "Image Sharpening", Value = "Off", Options = { "Off", "On" } },
                new FeatureSetting { Name = "Ambient Occlusion", Value = "Performance", Options = { "Off", "Performance", "Quality" } },
                new FeatureSetting { Name = "Anisotropic filtering", Value = "Application-controlled", Options = { "Application-controlled", "Off", "2x", "4x", "8x", "16x" } },
                new FeatureSetting { Name = "Antialiasing - FXAA", Value = "Off", Options = { "Off", "On" } },
                new FeatureSetting { Name = "Antialiasing - Gamma correction", Value = "On", Options = { "Off", "On" } },
                new FeatureSetting { Name = "Antialiasing - Mode", Value = "Application-controlled", Options = { "Application-controlled", "Off", "Enhance the application setting", "Override any application setting" } },
                new FeatureSetting { Name = "Background Application Max Frame Rate", Value = "Off", Options = { "Off", "On" } },
                new FeatureSetting { Name = "CUDA - GPUs", Value = "All", Options = { "All", "None" } },
                new FeatureSetting { Name = "DSR - Factors", Value = "Off", Options = { "Off", "1.20x", "1.50x", "2.00x", "4.00x" } },
                new FeatureSetting { Name = "Low Latency Mode", Value = "Off", Options = { "Off", "On", "Ultra" } },
                new FeatureSetting { Name = "Max Frame Rate", Value = "Off", Options = { "Off", "On" } },
                new FeatureSetting { Name = "Monitor Technology", Value = "G-SYNC Compatible", Options = { "Fixed Refresh", "G-SYNC Compatible" } },
                new FeatureSetting { Name = "Multi-Frame Sampled AA (MFAA)", Value = "Off", Options = { "Off", "On" } },
                new FeatureSetting { Name = "OpenGL rendering GPU", Value = "Auto-select", Options = { "Auto-select", "NVIDIA GeForce GTX 1650" } },
                new FeatureSetting { Name = "Power management mode", Value = "Normal", Options = { "Normal", "Prefer maximum performance" } },
                new FeatureSetting { Name = "Preferred refresh rate", Value = "Highest available", Options = { "Application-controlled", "Highest available" } },
                new FeatureSetting { Name = "Shader Cache Size", Value = "Driver Default", Options = { "Driver Default", "Disabled", "Unlimited", "10 GB", "100 GB" } },
                new FeatureSetting { Name = "Texture filtering - Anisotropic sample optimization", Value = "Off", Options = { "Off", "On" } },
                new FeatureSetting { Name = "Texture filtering - Negative LOD bias", Value = "Allow", Options = { "Allow", "Clamp" } },
                new FeatureSetting { Name = "Texture filtering - Quality", Value = "Quality", Options = { "High Quality", "Quality", "Performance", "High Performance" } },
                new FeatureSetting { Name = "Texture filtering - Trilinear optimization", Value = "On", Options = { "Off", "On" } },
                new FeatureSetting { Name = "Threaded optimization", Value = "Auto", Options = { "Auto", "Off", "On" } },
                new FeatureSetting { Name = "Triple buffering", Value = "Off", Options = { "Off", "On" } },
                new FeatureSetting { Name = "Vertical sync", Value = "Use the 3D application setting", Options = { "Use the 3D application setting", "Off", "On", "Adaptive", "Adaptive (half refresh rate)", "Fast" } },
                new FeatureSetting { Name = "Virtual Reality pre-rendered frames", Value = "1", Options = { "1", "2", "3", "4" } },
            };
        }

        private void LoadSettings()
        {
            var loaded = this._settingsService.Load3DSettings();
            if (loaded != null && loaded.Count > 0)
            {
                foreach (var setting in loaded)
                {
                    this.Settings.Add(setting);
                }
            }
            else
            {
                this.ExecuteRestoreDefaults(null);
            }
        }

        private void ExecuteApply(object? obj)
        {
            this._settingsService.Save3DSettings(this.Settings);
        }

        private void ExecuteRestoreDefaults(object? obj)
        {
            this.Settings.Clear();
            var defaults = GetDefaultSettings();
            foreach (var setting in defaults)
            {
                this.Settings.Add(setting);
            }
        }
    }
}
