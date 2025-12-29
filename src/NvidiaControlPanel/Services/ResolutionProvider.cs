// <copyright file="ResolutionProvider.cs" company="NvidiaControlPanel">
// Copyright (c) NvidiaControlPanel. All rights reserved.
// </copyright>

using System.Collections.Generic;
using System.Collections.ObjectModel;
using NvidiaControlPanel.Models;

namespace NvidiaControlPanel.Services
{
    /// <summary>
    /// Provides a list of simulated resolutions and refresh rates.
    /// </summary>
    public static class ResolutionProvider
    {
        /// <summary>
        /// Gets the list of available simulated resolutions.
        /// </summary>
        /// <returns>A collection of resolutions.</returns>
        public static Collection<Resolution> GetAvailableResolutions()
        {
            return new Collection<Resolution>
            {
                new Resolution
                {
                    Width = 2560,
                    Height = 1440,
                    RefreshRates = { 60, 120, 144 },
                },
                new Resolution
                {
                    Width = 1920,
                    Height = 1080,
                    RefreshRates = { 60, 75, 120, 144 },
                },
            };
        }
    }
}
