using System.Collections.ObjectModel;

namespace NvidiaControlPanel.Models
{
    /// <summary>
    /// Represents a single 3D setting feature.
    /// </summary>
    public class FeatureSetting
    {
        /// <summary>
        /// Gets or sets the name of the feature.
        /// </summary>
        public string Name { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the current value of the feature.
        /// </summary>
        public string Value { get; set; } = string.Empty;

        /// <summary>
        /// Gets the available options for the feature.
        /// </summary>
        public Collection<string> Options { get; } = new Collection<string>();

        /// <summary>
        /// Gets or sets a value indicating whether this is a global setting.
        /// </summary>
        public bool IsGlobal { get; set; }
    }
}
