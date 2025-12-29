// <copyright file="IDisplayService.cs" company="NvidiaControlPanel">
// Copyright (c) NvidiaControlPanel. All rights reserved.
// </copyright>

using System.Collections.ObjectModel;
using NvidiaControlPanel.Models;

namespace NvidiaControlPanel.Services
{
    /// <summary>
    /// Service interface for retrieving display resolution information.
    /// </summary>
    public interface IDisplayService
    {
        /// <summary>
        /// Gets the available display resolutions.
        /// </summary>
        /// <returns>A collection of available resolutions.</returns>
        ObservableCollection<Resolution> GetAvailableResolutions();
    }
}
