// <copyright file="Resolution.cs" company="NvidiaControlPanel">
// Copyright (c) NvidiaControlPanel. All rights reserved.
// </copyright>

using System.Collections.ObjectModel;

namespace NvidiaControlPanel.Models
{
    /// <summary>
    /// Represents a display resolution with associated refresh rates.
    /// </summary>
    public class Resolution
    {
        /// <summary>
        /// Gets or sets the width in pixels.
        /// </summary>
        public int Width { get; set; }

        /// <summary>
        /// Gets or sets the height in pixels.
        /// </summary>
        public int Height { get; set; }

        /// <summary>
        /// Gets the collection of available refresh rates in Hz.
        /// </summary>
        public Collection<int> RefreshRates { get; } = new Collection<int>();

        /// <summary>
        /// Gets the display name (e.g., "1920 x 1080").
        /// </summary>
        public string DisplayName => $"{this.Width} x {this.Height}";
    }
}
