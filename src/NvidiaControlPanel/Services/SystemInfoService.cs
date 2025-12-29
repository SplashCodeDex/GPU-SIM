using NvidiaControlPanel.Models;

namespace NvidiaControlPanel.Services
{
    /// <summary>
    /// Service that provides (spoofed) system information.
    /// </summary>
    public class SystemInfoService : ISystemInfoService
    {
        /// <inheritdoc/>
        public GpuInformation GetGpuInformation()
        {
            // In the future, this could load from a JSON config file.
            // For now, we return the hardcoded "Simulated" values.
            return new GpuInformation
            {
                GpuName = "NVIDIA GeForce GTX 1650",
                DriverVersion = "560.94",
                VideoMemory = "4096 MB GDDR5",
            };
        }
    }
}
