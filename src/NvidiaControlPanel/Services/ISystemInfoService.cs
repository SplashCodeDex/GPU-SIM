using System.Threading.Tasks;
using NvidiaControlPanel.Models;

namespace NvidiaControlPanel.Services
{
    /// <summary>
    /// Interface for retrieving system information (potentially spoofed).
    /// </summary>
    public interface ISystemInfoService
    {
        /// <summary>
        /// Gets the current GPU information asynchronously.
        /// </summary>
        /// <returns>A task that represents the asynchronous operation. The task result contains a <see cref="GpuInformation"/> object.</returns>
        Task<GpuInformation> GetGpuInformationAsync();

        /// <summary>
        /// Gets the current GPU information.
        /// </summary>
        /// <returns>A <see cref="GpuInformation"/> object.</returns>
        GpuInformation GetGpuInformation();
    }
}
