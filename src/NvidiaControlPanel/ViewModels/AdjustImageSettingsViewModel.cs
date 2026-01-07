// <copyright file="AdjustImageSettingsViewModel.cs" company="NvidiaControlPanel">
// Copyright (c) NvidiaControlPanel. All rights reserved.
// </copyright>

using System.Threading.Tasks;
using System.Windows;
using System.Windows.Input;
using NvidiaControlPanel.Services;
using NvidiaControlPanel.ViewModels.Core;

namespace NvidiaControlPanel.ViewModels
{
    /// <summary>
    /// ViewModel for the Adjust Image Settings with Preview page.
    /// </summary>
    public class AdjustImageSettingsViewModel : ViewModelBase, System.IDisposable
    {
        private readonly ISimulationService _simulationService;
        private bool _isPerformanceSelected;
        private bool _isBalancedSelected = true;
        private bool _isQualitySelected;
        private bool _useAdvancedSettings;
        private bool _useMyPreference = true;
        private bool _letApplicationDecide;
        private int _preferenceValue = 1;
        private bool _isApplying;
        private double _rotationAngle;
        private long _lastTicks;

        /// <summary>
        /// Initializes a new instance of the <see cref="AdjustImageSettingsViewModel"/> class.
        /// </summary>
        public AdjustImageSettingsViewModel()
            : this(new SimulationService())
        {
        }

        /// <summary>
        /// Initializes a new instance of the <see cref="AdjustImageSettingsViewModel"/> class with dependencies.
        /// </summary>
        /// <param name="simulationService">The simulation service.</param>
        public AdjustImageSettingsViewModel(ISimulationService simulationService)
        {
            this._simulationService = simulationService;
            this.ApplyCommand = new RelayCommand(this.ExecuteApply);

            this.LoadSettings();

            this._lastTicks = System.DateTime.UtcNow.Ticks;
            System.Windows.Media.CompositionTarget.Rendering += this.OnRendering;
        }

        /// <summary>
        /// Gets the rotation angle for the 3D preview.
        /// </summary>
        public double RotationAngle
        {
            get => this._rotationAngle;
            private set => this.SetProperty(ref this._rotationAngle, value);
        }

        /// <summary>
        /// Gets or sets a value indicating whether Performance is selected.
        /// </summary>
        public bool IsPerformanceSelected
        {
            get => this._isPerformanceSelected;
            set
            {
                if (this.SetProperty(ref this._isPerformanceSelected, value) && value)
                {
                    this.PreferenceValue = 0;
                }
            }
        }

        /// <summary>
        /// Gets or sets a value indicating whether Balanced is selected.
        /// </summary>
        public bool IsBalancedSelected
        {
            get => this._isBalancedSelected;
            set
            {
                if (this.SetProperty(ref this._isBalancedSelected, value) && value)
                {
                    this.PreferenceValue = 1;
                }
            }
        }

        /// <summary>
        /// Gets or sets a value indicating whether Quality is selected.
        /// </summary>
        public bool IsQualitySelected
        {
            get => this._isQualitySelected;
            set
            {
                if (this.SetProperty(ref this._isQualitySelected, value) && value)
                {
                    this.PreferenceValue = 2;
                }
            }
        }

        /// <summary>
        /// Gets or sets a value indicating whether to use advanced 3D image settings.
        /// </summary>
        public bool UseAdvancedSettings
        {
            get => this._useAdvancedSettings;
            set => this.SetProperty(ref this._useAdvancedSettings, value);
        }

        /// <summary>
        /// Gets or sets a value indicating whether to use user preferences.
        /// </summary>
        public bool UseMyPreference
        {
            get => this._useMyPreference;
            set => this.SetProperty(ref this._useMyPreference, value);
        }

        /// <summary>
        /// Gets or sets a value indicating whether to let the 3D application decide.
        /// </summary>
        public bool LetApplicationDecide
        {
            get => this._letApplicationDecide;
            set => this.SetProperty(ref this._letApplicationDecide, value);
        }

        /// <summary>
        /// Gets or sets the preference slider value (0-2).
        /// </summary>
        public int PreferenceValue
        {
            get => this._preferenceValue;
            set
            {
                if (this.SetProperty(ref this._preferenceValue, value))
                {
                    this.UpdateRadiosFromSlider();
                }
            }
        }

        /// <summary>
        /// Gets a value indicating whether settings are being applied.
        /// </summary>
        public bool IsApplying
        {
            get => this._isApplying;
            private set => this.SetProperty(ref this._isApplying, value);
        }

        /// <summary>
        /// Gets the command to apply settings.
        /// </summary>
        public ICommand ApplyCommand { get; }

        /// <summary>
        /// Gets the scale factor for pixelation effect (lower = more pixelated).
        /// </summary>
        public double PixelationScale
        {
            get
            {
                return this.PreferenceValue switch
                {
                    0 => 0.1, // Performance: Very pixelated
                    1 => 0.4, // Balanced: Slightly pixelated
                    _ => 1.0, // Quality: Full resolution
                };
            }
        }

        /// <summary>
        /// Gets the duration of one full rotation in seconds.
        /// </summary>
        public double RotationDuration
        {
            get
            {
                return this.PreferenceValue switch
                {
                    0 => 20.0, // Performance: Slow
                    1 => 10.0, // Balanced: Normal
                    _ => 5.0,  // Quality: Fast
                };
            }
        }

        /// <inheritdoc/>
        public void Dispose()
        {
            this.Dispose(true);
            System.GC.SuppressFinalize(this);
        }

        /// <summary>
        /// Releases resources used by the <see cref="AdjustImageSettingsViewModel"/> class.
        /// </summary>
        /// <param name="disposing">True if called from Dispose method.</param>
        protected virtual void Dispose(bool disposing)
        {
            if (disposing)
            {
                System.Windows.Media.CompositionTarget.Rendering -= this.OnRendering;
            }
        }

        private void OnRendering(object? sender, System.EventArgs e)
        {
            long currentTicks = System.DateTime.UtcNow.Ticks;
            double elapsedSeconds = (currentTicks - this._lastTicks) / (double)System.TimeSpan.TicksPerSecond;
            this._lastTicks = currentTicks;

            // Rotation speed (degrees per second)
            double degreesPerSecond = 360.0 / this.RotationDuration;
            this.RotationAngle = (this.RotationAngle + (degreesPerSecond * elapsedSeconds)) % 360;
        }

        private void LoadSettings()
        {
            var config = this._simulationService.GetConfig();
            this.PreferenceValue = config.PreferenceLevel;

            switch (config.ImageSettingsMode)
            {
                case "Advanced":
                    this.UseAdvancedSettings = true;
                    break;
                case "Preference":
                    this.UseMyPreference = true;
                    break;
                default:
                    this.LetApplicationDecide = true;
                    break;
            }
        }

        private void UpdateRadiosFromSlider()
        {
            this._isPerformanceSelected = this.PreferenceValue == 0;
            this._isBalancedSelected = this.PreferenceValue == 1;
            this._isQualitySelected = this.PreferenceValue == 2;

            this.OnPropertyChanged(nameof(this.IsPerformanceSelected));
            this.OnPropertyChanged(nameof(this.IsBalancedSelected));
            this.OnPropertyChanged(nameof(this.IsQualitySelected));
            this.OnPropertyChanged(nameof(this.PixelationScale));
            this.OnPropertyChanged(nameof(this.RotationDuration));
        }

        private async void ExecuteApply(object? obj)
        {
            this.IsApplying = true;
            Mouse.OverrideCursor = Cursors.Wait;

            try
            {
                // Simulate driver work
                await Task.Delay(1000).ConfigureAwait(true);

                var config = this._simulationService.GetConfig();
                config.PreferenceLevel = this.PreferenceValue;

                if (this.UseAdvancedSettings)
                {
                    config.ImageSettingsMode = "Advanced";
                }
                else if (this.UseMyPreference)
                {
                    config.ImageSettingsMode = "Preference";
                }
                else
                {
                    config.ImageSettingsMode = "Decide";
                }

                this._simulationService.SaveConfig(config);

                MessageBox.Show(
                    "3D Settings Applied.",
                    "NVIDIA Control Panel",
                    MessageBoxButton.OK,
                    MessageBoxImage.Information);
            }
            finally
            {
                Mouse.OverrideCursor = null;
                this.IsApplying = false;
            }
        }
    }
}
