// <copyright file="IRegistrySpoofService.cs" company="NvidiaControlPanel">
// Copyright (c) NvidiaControlPanel. All rights reserved.
// </copyright>

using NvidiaControlPanel.Models;

namespace NvidiaControlPanel.Services
{
    /// <summary>
    /// Interface for applying GPU information to the Windows Registry.
    /// </summary>
    public interface IRegistrySpoofService
    {
        /// <summary>
        /// Gets a value indicating whether the current process is running with Administrator privileges.
        /// </summary>
        /// <returns>True if elevated, otherwise false.</returns>
        bool IsElevated();

        /// <summary>
        /// Applies the spoofed GPU information to the registry.
        /// </summary>
        /// <param name="info">The GPU information to apply.</param>
        /// <returns>True if successful, otherwise false.</returns>
        bool ApplySpoof(GpuInformation info);
    }
}
