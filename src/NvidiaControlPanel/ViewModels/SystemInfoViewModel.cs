// <copyright file="SystemInfoViewModel.cs" company="NvidiaControlPanel">
// Copyright (c) NvidiaControlPanel. All rights reserved.
// </copyright>

using System.Windows;
using System.Windows.Input;
using NvidiaControlPanel.Models;
using NvidiaControlPanel.Services;
using NvidiaControlPanel.ViewModels.Core;

namespace NvidiaControlPanel.ViewModels
{
    /// <summary>
    /// ViewModel for the System Information window.
    /// </summary>
    public class SystemInfoViewModel : ViewModelBase
    {
        private readonly IRegistrySpoofService _registrySpoofService;
        private GpuInformation _gpuInfo;

        /// <summary>
        /// Initializes a new instance of the <see cref="SystemInfoViewModel"/> class.
        /// </summary>
        /// <param name="gpuInfo">The GPU information to display.</param>
        public SystemInfoViewModel(GpuInformation gpuInfo)
            : this(gpuInfo, new RegistrySpoofService())
        {
        }

        /// <summary>
        /// Initializes a new instance of the <see cref="SystemInfoViewModel"/> class with dependencies.
        /// </summary>
        /// <param name="gpuInfo">The GPU information.</param>
        /// <param name="registrySpoofService">The registry spoof service.</param>
        public SystemInfoViewModel(GpuInformation gpuInfo, IRegistrySpoofService registrySpoofService)
        {
            this._gpuInfo = gpuInfo;
            this._registrySpoofService = registrySpoofService;
            this.CloseCommand = new RelayCommand(this.ExecuteClose);
            this.ApplyRegistrySpoofCommand = new RelayCommand(this.ExecuteApplyRegistrySpoof);
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

        /// <summary>
        /// Gets the command to apply the registry spoof.
        /// </summary>
        public ICommand ApplyRegistrySpoofCommand { get; }

        private void ExecuteClose(object? obj)
        {
            if (obj is Window window)
            {
                window.Close();
            }
        }

        private void ExecuteApplyRegistrySpoof(object? obj)
        {
            bool success = this._registrySpoofService.ApplySpoof(this._gpuInfo);

            if (success)
            {
                MessageBox.Show(
                    "The NVIDIA driver settings have been successfully updated. Please restart any open hardware monitoring tools to see the changes.",
                    "NVIDIA Control Panel",
                    MessageBoxButton.OK,
                    MessageBoxImage.Information);
            }
            else
            {
                MessageBox.Show(
                    "Failed to update NVIDIA driver settings. Ensure you have the necessary permissions.",
                    "NVIDIA Control Panel Error",
                    MessageBoxButton.OK,
                    MessageBoxImage.Error);
            }
        }
    }
}
