using NvidiaControlPanel.Models;

namespace NvidiaControlPanel.Services
{
    /// <summary>
    /// Interface for retrieving system information (potentially spoofed).
    /// </summary>
    public interface ISystemInfoService
    {
        /// <summary>
        /// Gets the current GPU information.
        /// </summary>
        /// <returns>A <see cref="GpuInformation"/> object.</returns>
        GpuInformation GetGpuInformation();
    }
}
