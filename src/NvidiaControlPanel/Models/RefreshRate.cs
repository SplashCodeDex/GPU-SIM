// <copyright file="RefreshRate.cs" company="NvidiaControlPanel">
// Copyright (c) NvidiaControlPanel. All rights reserved.
// </copyright>

namespace NvidiaControlPanel.Models
{
    /// <summary>
    /// Represents a display refresh rate.
    /// </summary>
    public class RefreshRate
    {
        /// <summary>
        /// Gets or sets the refresh rate value in Hz.
        /// </summary>
        public int Value { get; set; }

        /// <summary>
        /// Gets or sets a value indicating whether this is an elite (high-end) refresh rate.
        /// </summary>
        public bool IsElite { get; set; }

        /// <inheritdoc/>
        public override string ToString() => $"{this.Value} Hz";
    }
}
