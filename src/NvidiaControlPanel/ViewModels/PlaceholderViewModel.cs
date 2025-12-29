// <copyright file="PlaceholderViewModel.cs" company="NvidiaControlPanel">
// Copyright (c) NvidiaControlPanel. All rights reserved.
// </copyright>

using NvidiaControlPanel.ViewModels.Core;

namespace NvidiaControlPanel.ViewModels
{
    /// <summary>
    /// A generic ViewModel for placeholder pages.
    /// </summary>
    public class PlaceholderViewModel : ViewModelBase
    {
        private string _title;
        private string _message;

        /// <summary>
        /// Initializes a new instance of the <see cref="PlaceholderViewModel"/> class.
        /// </summary>
        /// <param name="title">The title of the page.</param>
        public PlaceholderViewModel(string title)
        {
            this._title = title;
            this._message = "This feature is coming soon.";
        }

        /// <summary>
        /// Gets or sets the title of the page.
        /// </summary>
        public string Title
        {
            get => this._title;
            set => this.SetProperty(ref this._title, value);
        }

        /// <summary>
        /// Gets or sets the message to display.
        /// </summary>
        public string Message
        {
            get => this._message;
            set => this.SetProperty(ref this._message, value);
        }
    }
}
