// <copyright file="IAutoStartService.cs" company="NvidiaControlPanel">
// Copyright (c) NvidiaControlPanel. All rights reserved.
// </copyright>

namespace NvidiaControlPanel.Services
{
    /// <summary>
    /// Interface for managing application auto-start with Windows.
    /// </summary>
    public interface IAutoStartService
    {
        /// <summary>
        /// Gets a value indicating whether auto-start is currently enabled.
        /// </summary>
        /// <returns>True if enabled, otherwise false.</returns>
        bool IsEnabled();

        /// <summary>
        /// Enables auto-start for the application.
        /// </summary>
        /// <returns>True if successful, otherwise false.</returns>
        bool Enable();

        /// <summary>
        /// Disables auto-start for the application.
        /// </summary>
        /// <returns>True if successful, otherwise false.</returns>
        bool Disable();
    }
}
