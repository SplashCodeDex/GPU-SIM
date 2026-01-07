// <copyright file="HomeViewModel.cs" company="NvidiaControlPanel">
// Copyright (c) NvidiaControlPanel. All rights reserved.
// </copyright>

using NvidiaControlPanel.Models;
using NvidiaControlPanel.ViewModels.Core;

namespace NvidiaControlPanel.ViewModels
{
    /// <summary>
    /// ViewModel for the Home/Welcome page.
    /// </summary>
    public class HomeViewModel : ViewModelBase
    {
        private readonly GpuInformation _gpuInfo;

        /// <summary>
        /// Initializes a new instance of the <see cref="HomeViewModel"/> class.
        /// </summary>
        /// <param name="gpuInfo">The GPU information.</param>
        public HomeViewModel(GpuInformation gpuInfo)
        {
            this._gpuInfo = gpuInfo;
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
        /// Gets the Device Name.
        /// </summary>
        public string DeviceName => this._gpuInfo.DeviceName;

        /// <summary>
        /// Gets the Processor info.
        /// </summary>
        public string Processor => this._gpuInfo.Processor;

        /// <summary>
        /// Gets the Installed RAM.
        /// </summary>
        public string InstalledRam => this._gpuInfo.InstalledRam;

        /// <summary>
        /// Gets the System Type.
        /// </summary>
        public string SystemType => this._gpuInfo.SystemType;
    }
}
