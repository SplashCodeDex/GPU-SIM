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
    public class AdjustImageSettingsViewModel : ViewModelBase
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