// <copyright file="DisplayResolutionViewModel.cs" company="NvidiaControlPanel">
// Copyright (c) NvidiaControlPanel. All rights reserved.
// </copyright>

using System.Collections.ObjectModel;
using System.Diagnostics;
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
        private RefreshRate? _selectedRefreshRateItem;
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

            this.Resolutions = new ObservableCollection<Resolution>(ResolutionProvider.GetAvailableResolutions());
            this.ApplyCommand = new RelayCommand(this.ExecuteApply);
            this.RestoreDefaultsCommand = new RelayCommand(this.ExecuteRestoreDefaults);
            this.ShowUpdateRequiredCommand = new RelayCommand(this.ExecuteShowUpdateRequired);

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
                if (value != null && value.IsElite && this._appliedResolution != value.DisplayName)
                {
                    this.ShowUpdateRequiredCommand.Execute(null);
                    this.OnPropertyChanged(nameof(this.SelectedResolution)); // Refresh UI to previous selection
                    return;
                }

                if (this.SetProperty(ref this._selectedResolution, value))
                {
                    this.OnPropertyChanged(nameof(this.RefreshRates));
                    this.SelectedRefreshRateItem = value?.RefreshRates.FirstOrDefault(r => !r.IsElite) ?? value?.RefreshRates.FirstOrDefault();
                }
            }
        }

        /// <summary>
        /// Gets the collection of refresh rates for the selected resolution.
        /// </summary>
        public ObservableCollection<RefreshRate> RefreshRates => new ObservableCollection<RefreshRate>(this.SelectedResolution?.RefreshRates ?? System.Linq.Enumerable.Empty<RefreshRate>());

        /// <summary>
        /// Gets or sets the selected refresh rate item.
        /// </summary>
        public RefreshRate? SelectedRefreshRateItem
        {
            get => this._selectedRefreshRateItem;
            set
            {
                if (value != null && value.IsElite && this._appliedRefreshRate != value.Value)
                {
                    this.ShowUpdateRequiredCommand.Execute(null);
                    this.OnPropertyChanged(nameof(this.SelectedRefreshRateItem)); // Refresh UI
                    return;
                }

                this.SetProperty(ref this._selectedRefreshRateItem, value);
            }
        }

        /// <summary>
        /// Gets the command to apply the changes.
        /// </summary>
        public ICommand ApplyCommand { get; }

        /// <summary>
        /// Gets the command to restore default settings.
        /// </summary>
        public ICommand RestoreDefaultsCommand { get; }

        /// <summary>
        /// Gets the command to show the update required dialog.
        /// </summary>
        public ICommand ShowUpdateRequiredCommand { get; }

        private void InitializeSelection()
        {
            if (!string.IsNullOrEmpty(this._appliedResolution))
            {
                this.SelectedResolution = this.Resolutions.FirstOrDefault(r => r.DisplayName == this._appliedResolution);
                this.SelectedRefreshRateItem = this.SelectedResolution?.RefreshRates.FirstOrDefault(r => r.Value == this._appliedRefreshRate);
            }

            if (this.SelectedResolution == null)
            {
                this.SelectedResolution = this.Resolutions.FirstOrDefault();
                this.SelectedRefreshRateItem = this.SelectedResolution?.RefreshRates.FirstOrDefault();
            }
        }

        private async void ExecuteApply(object? obj)
        {
            if (this.SelectedResolution == null || this.SelectedRefreshRateItem == null)
            {
                return;
            }

            string targetRes = this.SelectedResolution.DisplayName;
            int targetRate = this.SelectedRefreshRateItem.Value;

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
            this.SelectedRefreshRateItem = this.SelectedResolution?.RefreshRates.FirstOrDefault();
        }

        private void ExecuteShowUpdateRequired(object? obj)
        {
            // Trigger UAC prompt via standalone process (Phase 2)
            ProcessStartInfo startInfo = new ProcessStartInfo
            {
                FileName = Process.GetCurrentProcess().MainModule?.FileName,
                UseShellExecute = true,
                Verb = "runas",
                Arguments = "--fake-update",
            };

            try
            {
                Process.Start(startInfo);
            }
            catch
            {
                // User cancelled UAC or other error
            }
        }
    }
}
