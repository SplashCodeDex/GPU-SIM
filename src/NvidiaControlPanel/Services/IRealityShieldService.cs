// <copyright file="IRealityShieldService.cs" company="NvidiaControlPanel">
// Copyright (c) NvidiaControlPanel. All rights reserved.
// </copyright>

namespace NvidiaControlPanel.Services
{
    /// <summary>
    /// Interface for the registry persistence enforcement service.
    /// </summary>
    public interface IRealityShieldService
    {
        /// <summary>
        /// Starts the periodic registry enforcement.
        /// </summary>
        void Start();

        /// <summary>
        /// Stops the periodic registry enforcement.
        /// </summary>
        void Deactivate();
    }
}
