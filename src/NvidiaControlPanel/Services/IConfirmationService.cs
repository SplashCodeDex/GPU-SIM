// <copyright file="IConfirmationService.cs" company="NvidiaControlPanel">
// Copyright (c) NvidiaControlPanel. All rights reserved.
// </copyright>

using System.Threading.Tasks;

namespace NvidiaControlPanel.Services
{
    /// <summary>
    /// Interface for showing a timed confirmation dialog.
    /// </summary>
    public interface IConfirmationService
    {
        /// <summary>
        /// Shows a confirmation dialog with a countdown.
        /// </summary>
        /// <param name="message">The message to display.</param>
        /// <param name="timeoutSeconds">The countdown duration in seconds.</param>
        /// <returns>A task that represents the asynchronous operation. The task result is true if the user confirmed, false if they declined or it timed out.</returns>
        Task<bool> ShowConfirmationAsync(string message, int timeoutSeconds);
    }
}
