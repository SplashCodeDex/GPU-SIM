// <copyright file="ConfirmationService.cs" company="NvidiaControlPanel">
// Copyright (c) NvidiaControlPanel. All rights reserved.
// </copyright>

using System.Threading.Tasks;
using System.Windows;
using NvidiaControlPanel.Views;

namespace NvidiaControlPanel.Services
{
    /// <summary>
    /// Implementation of the confirmation service.
    /// </summary>
    public class ConfirmationService : IConfirmationService
    {
        /// <inheritdoc/>
        public async Task<bool> ShowConfirmationAsync(string message, int timeoutSeconds)
        {
            // We need to ensure this runs on the UI thread and returns the result
            return await Application.Current.Dispatcher.InvokeAsync(() =>
            {
                var dialog = new ConfirmationDialogView(timeoutSeconds);
                dialog.Owner = Application.Current.MainWindow;
                bool? result = dialog.ShowDialog();
                return dialog.Result;
            });
        }
    }
}
