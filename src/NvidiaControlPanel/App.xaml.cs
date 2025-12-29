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

            base.OnStartup(e);

            this._trayIconService = new TrayIconService();
            this._trayIconService.Show();
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
    }
}
