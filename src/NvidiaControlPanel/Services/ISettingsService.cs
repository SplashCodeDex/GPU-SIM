// <copyright file="ISettingsService.cs" company="NvidiaControlPanel">
// Copyright (c) NvidiaControlPanel. All rights reserved.
// </copyright>

using System.Collections.Generic;
using System.Collections.ObjectModel;
using NvidiaControlPanel.Models;

namespace NvidiaControlPanel.Services
{
    /// <summary>
    /// Service for managing application settings persistence.
    /// </summary>
    public interface ISettingsService
    {
        /// <summary>
        /// Loads the 3D settings from storage.
        /// </summary>
        /// <returns>A collection of feature settings.</returns>
        Collection<FeatureSetting> Load3DSettings();

        /// <summary>
        /// Saves the 3D settings to storage.
        /// </summary>
        /// <param name="settings">The settings to save.</param>
        void Save3DSettings(IEnumerable<FeatureSetting> settings);

        /// <summary>
        /// Gets the list of available programs for customization.
        /// </summary>
        /// <returns>A collection of program names.</returns>
        Collection<string> GetAvailablePrograms();
    }
}
