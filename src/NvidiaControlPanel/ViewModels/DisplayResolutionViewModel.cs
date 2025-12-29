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
        private Resolution? _selectedResolution;
        private int _selectedRefreshRate;

        /// <summary>
        /// Initializes a new instance of the <see cref="DisplayResolutionViewModel"/> class.
        /// </summary>
        public DisplayResolutionViewModel()
            : this(new MockDisplayService())
        {
        }

        /// <summary>
        /// Initializes a new instance of the <see cref="DisplayResolutionViewModel"/> class with dependencies.
        /// </summary>
        /// <param name="displayService">The display service.</param>
        public DisplayResolutionViewModel(IDisplayService displayService)
        {
            this._displayService = displayService;
            this.Resolutions = this._displayService.GetAvailableResolutions();
            this.ApplyCommand = new RelayCommand(this.ExecuteApply);

            // Default selection
            this.SelectedResolution = this.Resolutions.FirstOrDefault();
            if (this.SelectedResolution != null)
            {
                this.SelectedRefreshRate = this.SelectedResolution.RefreshRates.FirstOrDefault();
            }
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

        private void ExecuteApply(object? obj)
        {
            if (this.SelectedResolution != null)
            {
                MessageBox.Show(
                    $"Resolution changed to {this.SelectedResolution.DisplayName} at {this.SelectedRefreshRate}Hz",
                    "Success",
                    MessageBoxButton.OK,
                    MessageBoxImage.Information);
            }
        }
    }
}
