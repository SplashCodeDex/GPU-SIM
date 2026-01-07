// <copyright file="App.xaml.cs" company="NvidiaControlPanel">
// Copyright (c) NvidiaControlPanel. All rights reserved.
// </copyright>

using System;
using System.Linq;
using System.Windows;
using NvidiaControlPanel.Services;

namespace NvidiaControlPanel
{
    /// <summary>
    /// Interaction logic for App.xaml.
    /// </summary>
    public partial class App : Application, IDisposable
    {
        private TrayIconService? _trayIconService;
        private RealityShieldService? _realityShieldService;

        /// <inheritdoc/>
        public void Dispose()
        {
            this.Dispose(true);
            GC.SuppressFinalize(this);
        }

        /// <summary>
        /// Releases resources used by the <see cref="App"/> class.
        /// </summary>
        /// <param name="disposing">True if called from Dispose method.</param>
        protected virtual void Dispose(bool disposing)
        {
            if (disposing)
            {
                this._trayIconService?.Dispose();
                this._realityShieldService?.Dispose();
            }
        }

        /// <inheritdoc/>
        protected override void OnStartup(StartupEventArgs e)
        {
            ArgumentNullException.ThrowIfNull(e);

            if (e.Args.Contains("--apply-spoof"))
            {
                HandleRegistrySpoof();
                this.Shutdown(0);
                return;
            }

            if (e.Args.Contains("--enable-context-menu"))
            {
                new ContextMenuService().Enable();
                this.Shutdown(0);
                return;
            }

            if (e.Args.Contains("--disable-context-menu"))
            {
                new ContextMenuService().Disable();
                this.Shutdown(0);
                return;
            }

            if (e.Args.Contains("--fake-update"))
            {
                var view = new Views.FakeUpdateView();
                view.ShowDialog();
                this.Shutdown(0);
                return;
            }

            base.OnStartup(e);

            var systemInfo = new SystemInfoService();
            var registrySpoof = new RegistrySpoofService();
            var autoStart = new AutoStartService();

            // Automatic Elevation Flow for Reality-Shield
            if (!registrySpoof.IsElevated() && autoStart.IsEnabled())
            {
                // Trigger self-elevation
                ElevateSelf(e.Args);
                this.Shutdown(0);
                return;
            }

            this._trayIconService = new TrayIconService();
            this._trayIconService.Show();

            this._realityShieldService = new RealityShieldService(systemInfo, registrySpoof);
            this._realityShieldService.Start();

            if (e.Args.Contains("--silent"))
            {
                // Ensure main window doesn't show initially
                this.StartupUri = null;
            }
        }

        /// <inheritdoc/>
        protected override void OnExit(ExitEventArgs e)
        {
            if (this._trayIconService is IDisposable disposable)
            {
                disposable.Dispose();
            }

            base.OnExit(e);
        }

        private static void HandleRegistrySpoof()
        {
            try
            {
                var systemInfo = new SystemInfoService();
                var registrySpoof = new RegistrySpoofService();
                var info = systemInfo.GetGpuInformation();
                registrySpoof.ApplySpoof(info);
            }
            catch (Exception)
            {
                // Silent fail for child process
            }
        }

        private static void ElevateSelf(string[] args)
        {
            var startInfo = new System.Diagnostics.ProcessStartInfo
            {
                FileName = System.Diagnostics.Process.GetCurrentProcess().MainModule?.FileName,
                UseShellExecute = true,
                Verb = "runas",
                Arguments = string.Join(" ", args),
            };

            try
            {
                System.Diagnostics.Process.Start(startInfo);
            }
            catch
            {
                // User cancelled UAC
            }
        }
    }
}
