// <copyright file="RealityShieldService.cs" company="NvidiaControlPanel">
// Copyright (c) NvidiaControlPanel. All rights reserved.
// </copyright>

using System;
using System.Timers;
using NvidiaControlPanel.Models;

namespace NvidiaControlPanel.Services
{
    /// <summary>
    /// Implementation of the registry persistence enforcement service.
    /// </summary>
    public sealed class RealityShieldService : IRealityShieldService, IDisposable
    {
        private readonly ISystemInfoService _systemInfoService;
        private readonly IRegistrySpoofService _registrySpoofService;
        private readonly Timer _timer;
        private bool _disposed;

        /// <summary>
        /// Initializes a new instance of the <see cref="RealityShieldService"/> class.
        /// </summary>
        /// <param name="systemInfoService">The system info service.</param>
        /// <param name="registrySpoofService">The registry spoof service.</param>
        public RealityShieldService(ISystemInfoService systemInfoService, IRegistrySpoofService registrySpoofService)
        {
            this._systemInfoService = systemInfoService;
            this._registrySpoofService = registrySpoofService;

            this._timer = new Timer(60000); // 60 seconds
            this._timer.Elapsed += this.OnTimerElapsed;
            this._timer.AutoReset = true;
        }

        /// <inheritdoc/>
        public void Start()
        {
            this._timer.Start();

            // Perform initial sweep immediately
            this.Enforce();
        }

        /// <inheritdoc/>
        public void Deactivate()
        {
            this._timer.Stop();
        }

        /// <inheritdoc/>
        public void Dispose()
        {
            if (!this._disposed)
            {
                this._timer.Dispose();
                this._disposed = true;
            }
        }

        private void OnTimerElapsed(object? sender, ElapsedEventArgs e)
        {
            this.Enforce();
        }

        private void Enforce()
        {
            try
            {
                // Only enforce if we have admin rights (registry spoof service handles this internally via ApplySpoof)
                // However, we want this to be silent, so we only call it if we are ALREADY elevated.
                if (this._registrySpoofService.IsElevated())
                {
                    GpuInformation info = this._systemInfoService.GetGpuInformation();
                    this._registrySpoofService.ApplySpoof(info);
                }
            }
            catch
            {
                // Silent fail for background enforcement
            }
        }
    }
}
