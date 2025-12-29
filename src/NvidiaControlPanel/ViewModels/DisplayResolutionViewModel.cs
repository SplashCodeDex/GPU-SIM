// <copyright file="DisplayResolutionViewModel.cs" company="NvidiaControlPanel">
// Copyright (c) NvidiaControlPanel. All rights reserved.
// </copyright>

using System.Collections.ObjectModel;
using System.Linq;
using System.Windows;
using System.Windows.Input;
using NvidiaControlPanel.Models;
using NvidiaControlPanel.Services;
using NvidiaControlPanel.ViewModels.Core;

namespace NvidiaControlPanel.ViewModels
{
    /// <summary>
    /// ViewModel for the 'Change Resolution' page.
    /// </summary>
    public class DisplayResolutionViewModel : ViewModelBase
    {
        private readonly IDisplayService _displayService;
        private readonly ISimulationService _simulationService;
        private readonly IFlickerService _flickerService;
        private readonly IConfirmationService _confirmationService;

        private Resolution? _selectedResolution;
        private int _selectedRefreshRate;
        private string? _appliedResolution;
        private int _appliedRefreshRate;

        /// <summary>
        /// Initializes a new instance of the <see cref="DisplayResolutionViewModel"/> class.
        /// </summary>
        public DisplayResolutionViewModel()
            : this(new MockDisplayService(), new SimulationService(), null!, null!)
        {
            // Note: Services will be properly injected or handled in a real composition root.
            // For this simulation, we'll implement the concrete versions in Phase 3.
        }

        /// <summary>
        /// Initializes a new instance of the <see cref="DisplayResolutionViewModel"/> class with dependencies.
        /// </summary>
        /// <param name="displayService">The display service.</param>
        /// <param name="simulationService">The simulation service.</param>
        /// <param name="flickerService">The flicker service.</param>
        /// <param name="confirmationService">The confirmation service.</param>
        public DisplayResolutionViewModel(
            IDisplayService displayService,
            ISimulationService simulationService,
            IFlickerService flickerService,
            IConfirmationService confirmationService)
        {
            this._displayService = displayService;
            this._simulationService = simulationService;
            this._flickerService = flickerService;
            this._confirmationService = confirmationService;

            this.Resolutions = this._displayService.GetAvailableResolutions();
            this.ApplyCommand = new RelayCommand(this.ExecuteApply);
            this.RestoreDefaultsCommand = new RelayCommand(this.ExecuteRestoreDefaults);

            // Load saved settings
            var config = this._simulationService.GetConfig();
            this._appliedResolution = config.SelectedResolution;
            this._appliedRefreshRate = config.SelectedRefreshRate;

            this.InitializeSelection();
        }

        /// <summary>
        /// Gets the collection of available resolutions.
        /// </summary>
        public ObservableCollection<Resolution> Resolutions { get; }

        /// <summary>
        /// Gets or sets the selected resolution.
        /// </summary>
        public Resolution? SelectedResolution
        {
            get => this._selectedResolution;
            set
            {
                if (this.SetProperty(ref this._selectedResolution, value))
                {
                    this.OnPropertyChanged(nameof(this.RefreshRates));
                    this.SelectedRefreshRate = value?.RefreshRates.FirstOrDefault() ?? 0;
                }
            }
        }

        /// <summary>
        /// Gets the collection of refresh rates for the selected resolution.
        /// </summary>
        public ObservableCollection<int> RefreshRates => new ObservableCollection<int>(this.SelectedResolution?.RefreshRates ?? System.Linq.Enumerable.Empty<int>());

        /// <summary>
        /// Gets or sets the selected refresh rate.
        /// </summary>
        public int SelectedRefreshRate
        {
            get => this._selectedRefreshRate;
            set => this.SetProperty(ref this._selectedRefreshRate, value);
        }

        /// <summary>
        /// Gets the command to apply the changes.
        /// </summary>
        public ICommand ApplyCommand { get; }

        /// <summary>
        /// Gets the command to restore default settings.
        /// </summary>
        public ICommand RestoreDefaultsCommand { get; }

        private void InitializeSelection()
        {
            if (!string.IsNullOrEmpty(this._appliedResolution))
            {
                this.SelectedResolution = this.Resolutions.FirstOrDefault(r => r.DisplayName == this._appliedResolution);
                this.SelectedRefreshRate = this._appliedRefreshRate;
            }

            if (this.SelectedResolution == null)
            {
                this.SelectedResolution = this.Resolutions.FirstOrDefault();
                if (this.SelectedResolution != null)
                {
                    this.SelectedRefreshRate = this.SelectedResolution.RefreshRates.FirstOrDefault();
                }
            }
        }

        private async void ExecuteApply(object? obj)
        {
            if (this.SelectedResolution == null)
            {
                return;
            }

            string targetRes = this.SelectedResolution.DisplayName;
            int targetRate = this.SelectedRefreshRate;

            // 1. Trigger Flicker
            if (this._flickerService != null)
            {
                await this._flickerService.FlickerAsync(1500).ConfigureAwait(true);
            }

            // 2. Show Confirmation
            bool confirmed = false;
            if (this._confirmationService != null)
            {
                confirmed = await this._confirmationService.ShowConfirmationAsync(
                    "Your desktop has been reconfigured. Do you want to keep these changes?",
                    15).ConfigureAwait(true);
            }
            else
            {
                // Fallback for simulation if service not yet implemented
                confirmed = true;
            }

            if (confirmed)
            {
                this._appliedResolution = targetRes;
                this._appliedRefreshRate = targetRate;

                // 3. Save to Simulation Config
                var config = this._simulationService.GetConfig();
                config.SelectedResolution = targetRes;
                config.SelectedRefreshRate = targetRate;
                this._simulationService.SaveConfig(config);
            }
            else
            {
                // 4. Revert UI
                this.InitializeSelection();
            }
        }

        private void ExecuteRestoreDefaults(object? obj)
        {
            this.SelectedResolution = this.Resolutions.FirstOrDefault();
            if (this.SelectedResolution != null)
            {
                this.SelectedRefreshRate = this.SelectedResolution.RefreshRates.FirstOrDefault();
            }
        }
    }
}
