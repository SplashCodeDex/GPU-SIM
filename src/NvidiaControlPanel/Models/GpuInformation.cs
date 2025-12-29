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

        /// <summary>
        /// Gets or sets the bus support (e.g., "PCI Express x16 Gen 3").
        /// </summary>
        public string BusSupport { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the BIOS version (e.g., "90.06.33.00.70").
        /// </summary>
        public string BiosVersion { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the DirectX support level (e.g., "12 Ultimate").
        /// </summary>
        public string DirectXSupport { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the Device ID (e.g., "1F82").
        /// </summary>
        public string DeviceId { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the Vendor ID (e.g., "10DE").
        /// </summary>
        public string VendorId { get; set; } = string.Empty;
    }
}
