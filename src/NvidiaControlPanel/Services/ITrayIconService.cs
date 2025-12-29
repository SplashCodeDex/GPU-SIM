// <copyright file="ITrayIconService.cs" company="NvidiaControlPanel">
// Copyright (c) NvidiaControlPanel. All rights reserved.
// </copyright>

namespace NvidiaControlPanel.Services
{
    /// <summary>
    /// Interface for managing the system tray notification icon.
    /// </summary>
    public interface ITrayIconService
    {
        /// <summary>
        /// Shows the tray icon.
        /// </summary>
        void Show();

        /// <summary>
        /// Hides the tray icon.
        /// </summary>
        void Hide();

        /// <summary>
        /// Sets the visibility of the tray icon.
        /// </summary>
        /// <param name="visible">True to show, false to hide.</param>
        void SetVisibility(bool visible);
    }
}
