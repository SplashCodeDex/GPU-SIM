namespace NvidiaControlPanel.Services
{
    /// <summary>
    /// Represents the configuration for the simulation.
    /// </summary>
    public class SimulationConfig
    {
        /// <summary>
        /// Gets or sets the name of the GPU.
        /// </summary>
        public string GpuName { get; set; } = "NVIDIA GeForce GTX 1650";

        /// <summary>
        /// Gets or sets the driver version.
        /// </summary>
        public string DriverVersion { get; set; } = "536.23";

        /// <summary>
        /// Gets or sets the video memory.
        /// </summary>
        public string VideoMemory { get; set; } = "4096 MB GDDR5";

        /// <summary>
        /// Gets or sets the bus support.
        /// </summary>
        public string BusSupport { get; set; } = "PCI Express x16 Gen 3";

        /// <summary>
        /// Gets or sets the BIOS version.
        /// </summary>
        public string BiosVersion { get; set; } = "90.06.33.00.70";

        /// <summary>
        /// Gets or sets the DirectX support level.
        /// </summary>
        public string DirectXSupport { get; set; } = "12 Ultimate";

        /// <summary>
        /// Gets or sets the Device ID.
        /// </summary>
        public string DeviceId { get; set; } = "1F82";

        /// <summary>
        /// Gets or sets the Vendor ID.
        /// </summary>
        public string VendorId { get; set; } = "10DE";

        /// <summary>
        /// Gets or sets the selected resolution.
        /// </summary>
        public string SelectedResolution { get; set; } = "1920 x 1080";

        /// <summary>
        /// Gets or sets the selected refresh rate.
        /// </summary>
        public int SelectedRefreshRate { get; set; } = 60;

        /// <summary>
        /// Gets or sets the image settings mode.
        /// </summary>
        public string ImageSettingsMode { get; set; } = "Decide";

        /// <summary>
        /// Gets or sets the preference level.
        /// </summary>
        public int PreferenceLevel { get; set; } = 1;
    }
}
