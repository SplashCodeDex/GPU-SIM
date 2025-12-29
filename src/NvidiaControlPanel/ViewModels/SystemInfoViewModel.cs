// <copyright file="SystemInfoViewModel.cs" company="NvidiaControlPanel">
// Copyright (c) NvidiaControlPanel. All rights reserved.
// </copyright>

using System.Windows;
using System.Windows.Input;
using NvidiaControlPanel.Models;
using NvidiaControlPanel.ViewModels.Core;

namespace NvidiaControlPanel.ViewModels
{
    /// <summary>
    /// ViewModel for the System Information window.
    /// </summary>
    public class SystemInfoViewModel : ViewModelBase
    {
        private GpuInformation _gpuInfo;

        /// <summary>
        /// Initializes a new instance of the <see cref="SystemInfoViewModel"/> class.
        /// </summary>
        /// <param name="gpuInfo">The GPU information to display.</param>
        public SystemInfoViewModel(GpuInformation gpuInfo)
        {
            this._gpuInfo = gpuInfo;
            this.CloseCommand = new RelayCommand(this.ExecuteClose);
        }

        /// <summary>
        /// Gets the GPU Name.
        /// </summary>
        public string GpuName => this._gpuInfo.GpuName;

        /// <summary>
        /// Gets the Driver Version.
        /// </summary>
        public string DriverVersion => this._gpuInfo.DriverVersion;

        /// <summary>
        /// Gets the Video Memory.
        /// </summary>
        public string VideoMemory => this._gpuInfo.VideoMemory;

        /// <summary>
        /// Gets the Bus Support.
        /// </summary>
        public string BusSupport => this._gpuInfo.BusSupport;

        /// <summary>
        /// Gets the BIOS Version.
        /// </summary>
        public string BiosVersion => this._gpuInfo.BiosVersion;

        /// <summary>
        /// Gets the DirectX Support level.
        /// </summary>
        public string DirectXSupport => this._gpuInfo.DirectXSupport;

        /// <summary>
        /// Gets the Device ID.
        /// </summary>
        public string DeviceId => this._gpuInfo.DeviceId;

        /// <summary>
        /// Gets the Vendor ID.
        /// </summary>
        public string VendorId => this._gpuInfo.VendorId;

        /// <summary>
        /// Gets the command to close the window.
        /// </summary>
        public ICommand CloseCommand { get; }

        private void ExecuteClose(object? obj)
        {
            if (obj is Window window)
            {
                window.Close();
            }
        }
    }
}
