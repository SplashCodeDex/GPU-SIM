// <copyright file="IContextMenuService.cs" company="NvidiaControlPanel">
// Copyright (c) NvidiaControlPanel. All rights reserved.
// </copyright>

namespace NvidiaControlPanel.Services
{
    /// <summary>
    /// Interface for managing the desktop context menu entry.
    /// </summary>
    public interface IContextMenuService
    {
        /// <summary>
        /// Gets a value indicating whether the context menu entry is currently enabled.
        /// </summary>
        /// <returns>True if enabled, otherwise false.</returns>
        bool IsEnabled();

        /// <summary>
        /// Enables the desktop context menu entry.
        /// </summary>
        /// <returns>True if successful, otherwise false.</returns>
        bool Enable();

        /// <summary>
        /// Disables the desktop context menu entry.
        /// </summary>
        /// <returns>True if successful, otherwise false.</returns>
        bool Disable();
    }
}
