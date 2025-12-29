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
                new Resolution { Width = 3840, Height = 2160, RefreshRates = { 30, 60 } },
                new Resolution { Width = 2560, Height = 1440, RefreshRates = { 60, 120, 144 } },
                new Resolution { Width = 1920, Height = 1080, RefreshRates = { 60, 75, 120, 144, 240 } },
                new Resolution { Width = 1600, Height = 900, RefreshRates = { 60 } },
                new Resolution { Width = 1366, Height = 768, RefreshRates = { 60 } },
                new Resolution { Width = 1280, Height = 720, RefreshRates = { 60 } },
            };

            return resolutions;
        }
    }
}
