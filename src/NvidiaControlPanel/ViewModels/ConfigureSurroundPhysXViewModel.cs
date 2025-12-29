// <copyright file="ConfigureSurroundPhysXViewModel.cs" company="NvidiaControlPanel">
// Copyright (c) NvidiaControlPanel. All rights reserved.
// </copyright>

using System.Collections.ObjectModel;
using NvidiaControlPanel.Services;
using NvidiaControlPanel.ViewModels.Core;

namespace NvidiaControlPanel.ViewModels
{
    /// <summary>
    /// ViewModel for the Configure Surround, PhysX page.
    /// </summary>
    public class ConfigureSurroundPhysXViewModel : ViewModelBase
    {
        private string _selectedPhysXProcessor;
        private bool _isSurroundEnabled;

        /// <summary>
        /// Initializes a new instance of the <see cref="ConfigureSurroundPhysXViewModel"/> class.
        /// </summary>
        public ConfigureSurroundPhysXViewModel()
        {
            this._selectedPhysXProcessor = "Auto-select (Recommended)";
            this.PhysXProcessors.Add("Auto-select (Recommended)");
            this.PhysXProcessors.Add("GeForce GTX 1650");
            this.PhysXProcessors.Add("CPU");
        }

        /// <summary>
        /// Initializes a new instance of the <see cref="ConfigureSurroundPhysXViewModel"/> class with dependencies.
        /// </summary>
        /// <param name="systemInfoService">The system info service.</param>
        public ConfigureSurroundPhysXViewModel(ISystemInfoService systemInfoService)
            : this()
        {
            // In a real scenario, we'd fetch actual GPU names from the service.
        }

        /// <summary>
        /// Gets the collection of available PhysX processors.
        /// </summary>
        public ObservableCollection<string> PhysXProcessors { get; } = new ObservableCollection<string>();

        /// <summary>
        /// Gets or sets the selected PhysX processor.
        /// </summary>
        public string SelectedPhysXProcessor
        {
            get => this._selectedPhysXProcessor;
            set => this.SetProperty(ref this._selectedPhysXProcessor, value);
        }

        /// <summary>
        /// Gets or sets a value indicating whether Surround is enabled.
        /// </summary>
        public bool IsSurroundEnabled
        {
            get => this._isSurroundEnabled;
            set => this.SetProperty(ref this._isSurroundEnabled, value);
        }
    }
}