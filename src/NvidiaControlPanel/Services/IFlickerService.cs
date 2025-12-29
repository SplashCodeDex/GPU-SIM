// <copyright file="IFlickerService.cs" company="NvidiaControlPanel">
// Copyright (c) NvidiaControlPanel. All rights reserved.
// </copyright>

using System.Threading.Tasks;

namespace NvidiaControlPanel.Services
{
    /// <summary>
    /// Interface for simulating a screen flicker/mode switch.
    /// </summary>
    public interface IFlickerService
    {
        /// <summary>
        /// Triggers a screen flicker effect.
        /// </summary>
        /// <param name="durationMs">The duration of the flicker in milliseconds.</param>
        /// <returns>A task that represents the asynchronous operation.</returns>
        Task FlickerAsync(int durationMs);
    }
}
