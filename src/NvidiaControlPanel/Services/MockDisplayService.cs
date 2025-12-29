// <copyright file="MockDisplayService.cs" company="NvidiaControlPanel">
// Copyright (c) NvidiaControlPanel. All rights reserved.
// </copyright>

using System.Collections.ObjectModel;
using NvidiaControlPanel.Models;

namespace NvidiaControlPanel.Services
{
    /// <summary>
    /// Mock implementation of the display service.
    /// </summary>
    public class MockDisplayService : IDisplayService
    {
        /// <inheritdoc/>
        public ObservableCollection<Resolution> GetAvailableResolutions()
        {
            var resolutions = new ObservableCollection<Resolution>
            {
                new Resolution { Width = 3840, Height = 2160, IsElite = true, RefreshRates = { new RefreshRate { Value = 30 }, new RefreshRate { Value = 60 } } },
                new Resolution { Width = 2560, Height = 1440, IsElite = true, RefreshRates = { new RefreshRate { Value = 60 }, new RefreshRate { Value = 120, IsElite = true }, new RefreshRate { Value = 144, IsElite = true } } },
                new Resolution { Width = 1920, Height = 1080, IsElite = false, RefreshRates = { new RefreshRate { Value = 60 }, new RefreshRate { Value = 75, IsElite = true }, new RefreshRate { Value = 120, IsElite = true }, new RefreshRate { Value = 144, IsElite = true }, new RefreshRate { Value = 240, IsElite = true } } },
                new Resolution { Width = 1600, Height = 900, IsElite = false, RefreshRates = { new RefreshRate { Value = 60 } } },
                new Resolution { Width = 1366, Height = 768, IsElite = false, RefreshRates = { new RefreshRate { Value = 60 } } },
                new Resolution { Width = 1280, Height = 720, IsElite = false, RefreshRates = { new RefreshRate { Value = 60 } } },
            };

            return resolutions;
        }
    }
}
