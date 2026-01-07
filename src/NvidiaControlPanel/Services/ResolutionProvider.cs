// <copyright file="ResolutionProvider.cs" company="NvidiaControlPanel">
// Copyright (c) NvidiaControlPanel. All rights reserved.
// </copyright>

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
                    IsElite = true,
                    RefreshRates =
                    {
                        new RefreshRate { Value = 60, IsElite = false },
                        new RefreshRate { Value = 120, IsElite = true },
                        new RefreshRate { Value = 144, IsElite = true },
                    },
                },
                new Resolution
                {
                    Width = 1920,
                    Height = 1080,
                    IsElite = false,
                    RefreshRates =
                    {
                        new RefreshRate { Value = 60, IsElite = false },
                        new RefreshRate { Value = 75, IsElite = true },
                        new RefreshRate { Value = 120, IsElite = true },
                        new RefreshRate { Value = 144, IsElite = true },
                    },
                },
            };
        }
    }
}
