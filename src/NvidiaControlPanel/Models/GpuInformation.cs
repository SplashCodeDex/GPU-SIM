namespace NvidiaControlPanel.Models
{
    /// <summary>
    /// Represents the spoofed GPU information.
    /// </summary>
    public class GpuInformation
    {
        /// <summary>
        /// Gets or sets the name of the GPU (e.g., "NVIDIA GeForce GTX 1650").
        /// </summary>
        public string GpuName { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the driver version string (e.g., "560.94").
        /// </summary>
        public string DriverVersion { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the dedicated video memory size (e.g., "4096 MB").
        /// </summary>
        public string VideoMemory { get; set; } = string.Empty;
    }
}
