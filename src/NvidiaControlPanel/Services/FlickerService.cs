// <copyright file="FlickerService.cs" company="NvidiaControlPanel">
// Copyright (c) NvidiaControlPanel. All rights reserved.
// </copyright>

using System.Threading.Tasks;
using System.Windows;
using NvidiaControlPanel.Views;

namespace NvidiaControlPanel.Services
{
    /// <summary>
    /// Implementation of the flicker service.
    /// </summary>
    public class FlickerService : IFlickerService
    {
        /// <inheritdoc/>
        public async Task FlickerAsync(int durationMs)
        {
            var flickerWindow = new FlickerView();
            flickerWindow.Show();

            await Task.Delay(durationMs).ConfigureAwait(true);

            flickerWindow.Close();
        }
    }
}
