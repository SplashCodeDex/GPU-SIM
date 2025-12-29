// <copyright file="NavigationService.cs" company="NvidiaControlPanel">
// Copyright (c) NvidiaControlPanel. All rights reserved.
// </copyright>

using System.Collections.Generic;
using System.Linq;

namespace NvidiaControlPanel.Services
{
    /// <summary>
    /// Implementation of the navigation history service.
    /// </summary>
    public class NavigationService : INavigationService
    {
        private readonly Stack<string> _backStack = new Stack<string>();
        private readonly Stack<string> _forwardStack = new Stack<string>();
        private string? _currentView;

        /// <inheritdoc/>
        public bool CanGoBack => this._backStack.Count > 0;

        /// <inheritdoc/>
        public bool CanGoForward => this._forwardStack.Count > 0;

        /// <inheritdoc/>
        public string? PreviousViewName => this.CanGoBack ? GetDisplayName(this._backStack.Peek()) : null;

        /// <inheritdoc/>
        public string? NextViewName => this.CanGoForward ? GetDisplayName(this._forwardStack.Peek()) : null;

        /// <inheritdoc/>
        public void RecordNavigation(string viewName)
        {
            if (viewName == "Home" || viewName == this._currentView)
            {
                return;
            }

            if (this._currentView != null)
            {
                this._backStack.Push(this._currentView);
            }

            this._currentView = viewName;
            this._forwardStack.Clear();
        }

        /// <inheritdoc/>
        public string? GoBack()
        {
            if (!this.CanGoBack)
            {
                return null;
            }

            if (this._currentView != null)
            {
                this._forwardStack.Push(this._currentView);
            }

            this._currentView = this._backStack.Pop();
            return this._currentView;
        }

        /// <inheritdoc/>
        public string? GoForward()
        {
            if (!this.CanGoForward)
            {
                return null;
            }

            if (this._currentView != null)
            {
                this._backStack.Push(this._currentView);
            }

            this._currentView = this._forwardStack.Pop();
            return this._currentView;
        }

        private static string GetDisplayName(string viewName)
        {
            return viewName switch
            {
                "Manage3DSettings" => "Manage 3D settings",
                "ChangeResolution" => "Change resolution",
                "AdjustImageSettings" => "Adjust image settings with preview",
                "ConfigureSurroundPhysX" => "Configure Surround, PhysX",
                "AdjustDesktopColor" => "Adjust desktop color settings",
                "RotateDisplay" => "Rotate display",
                "ViewHDCPStatus" => "View HDCP status",
                "SetupDigitalAudio" => "Set up digital audio",
                "AdjustDesktopSizePosition" => "Adjust desktop size and position",
                "SetupMultipleDisplays" => "Set up multiple displays",
                "AdjustVideoColor" => "Adjust video color settings",
                "AdjustVideoImage" => "Adjust video image settings",
                "Home" => "Home",
                _ => viewName
            };
        }
    }
}
