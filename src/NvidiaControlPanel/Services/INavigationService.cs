// <copyright file="INavigationService.cs" company="NvidiaControlPanel">
// Copyright (c) NvidiaControlPanel. All rights reserved.
// </copyright>

namespace NvidiaControlPanel.Services
{
    /// <summary>
    /// Interface for navigation history service.
    /// </summary>
    public interface INavigationService
    {
        /// <summary>
        /// Gets a value indicating whether it is possible to navigate back.
        /// </summary>
        bool CanGoBack { get; }

        /// <summary>
        /// Gets a value indicating whether it is possible to navigate forward.
        /// </summary>
        bool CanGoForward { get; }

        /// <summary>
        /// Gets the name of the previous view in history.
        /// </summary>
        string? PreviousViewName { get; }

        /// <summary>
        /// Gets the name of the next view in history.
        /// </summary>
        string? NextViewName { get; }

        /// <summary>
        /// Records a navigation to a new view.
        /// </summary>
        /// <param name="viewName">The name of the view navigated to.</param>
        void RecordNavigation(string viewName);

        /// <summary>
        /// Navigates back in history.
        /// </summary>
        /// <returns>The view name to navigate back to.</returns>
        string? GoBack();

        /// <summary>
        /// Navigates forward in history.
        /// </summary>
        /// <returns>The view name to navigate forward to.</returns>
        string? GoForward();
    }
}
