using System.Threading.Tasks;
using NvidiaControlPanel.Models;

namespace NvidiaControlPanel.Services
{
    /// <summary>
    /// Provides system information about the simulated hardware.
    /// </summary>
    public class SystemInfoService : ISystemInfoService
    {
        /// <summary>
        /// The simulation service.
        /// </summary>
        private readonly ISimulationService _simulationService;

        /// <summary>
        /// Initializes a new instance of the <see cref="SystemInfoService"/> class.
        /// </summary>
        public SystemInfoService()
            : this(new SimulationService())
        {
        }

        /// <summary>
        /// Initializes a new instance of the <see cref="SystemInfoService"/> class.
        /// </summary>
        /// <param name="simulationService">The simulation service to use.</param>
        public SystemInfoService(ISimulationService simulationService)
        {
            this._simulationService = simulationService;
        }

        /// <inheritdoc/>
        public async Task<GpuInformation> GetGpuInformationAsync()
        {
            var config = await this._simulationService.GetConfigAsync().ConfigureAwait(false);

            return new GpuInformation
            {
                GpuName = config.GpuName,
                DriverVersion = config.DriverVersion,
                VideoMemory = config.VideoMemory,
                BusSupport = config.BusSupport,
                BiosVersion = config.BiosVersion,
                DirectXSupport = config.DirectXSupport,
                DeviceId = config.DeviceId,
                VendorId = config.VendorId,
                DeviceName = config.DeviceName,
                Processor = config.Processor,
                InstalledRam = config.InstalledRam,
                SystemType = config.SystemType,
                SelectedResolution = config.SelectedResolution,
                SelectedRefreshRate = config.SelectedRefreshRate,
                ImageSettingsMode = config.ImageSettingsMode,
                PreferenceLevel = config.PreferenceLevel,
                IsContextMenuEnabled = config.IsContextMenuEnabled,
                IsTrayIconVisible = config.IsTrayIconVisible,
            };
        }

        /// <inheritdoc/>
        public GpuInformation GetGpuInformation()
        {
            var config = this._simulationService.GetConfig();

            return new GpuInformation
            {
                GpuName = config.GpuName,
                DriverVersion = config.DriverVersion,
                VideoMemory = config.VideoMemory,
                BusSupport = config.BusSupport,
                BiosVersion = config.BiosVersion,
                DirectXSupport = config.DirectXSupport,
                DeviceId = config.DeviceId,
                VendorId = config.VendorId,
                DeviceName = config.DeviceName,
                Processor = config.Processor,
                InstalledRam = config.InstalledRam,
                SystemType = config.SystemType,
                SelectedResolution = config.SelectedResolution,
                SelectedRefreshRate = config.SelectedRefreshRate,
                ImageSettingsMode = config.ImageSettingsMode,
                PreferenceLevel = config.PreferenceLevel,
                IsContextMenuEnabled = config.IsContextMenuEnabled,
                IsTrayIconVisible = config.IsTrayIconVisible,
            };
        }
    }
}
