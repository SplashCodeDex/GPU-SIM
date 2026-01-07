// <copyright file="FakeUpdateViewModel.cs" company="NvidiaControlPanel">
// Copyright (c) NvidiaControlPanel. All rights reserved.
// </copyright>

using System;
using System.Windows.Input;
using System.Windows.Threading;
using NvidiaControlPanel.ViewModels.Core;

namespace NvidiaControlPanel.ViewModels
{
    /// <summary>
    /// ViewModel for the fake NVIDIA update dialog.
    /// </summary>
    public class FakeUpdateViewModel : ViewModelBase
    {
        private readonly DispatcherTimer _timer;
        private double _progressValue;
        private string _statusMessage = "Checking for updates...";
        private bool _isErrorVisible;
        private int _step;

        /// <summary>
        /// Initializes a new instance of the <see cref="FakeUpdateViewModel"/> class.
        /// </summary>
        public FakeUpdateViewModel()
        {
            this.CloseCommand = new RelayCommand(o => ((System.Windows.Window)o!).Close());

            this._timer = new DispatcherTimer();
            this._timer.Interval = TimeSpan.FromMilliseconds(100);
            this._timer.Tick += this.Timer_Tick;
            this._timer.Start();
        }

        /// <summary>
        /// Gets or sets the current progress value.
        /// </summary>
        public double ProgressValue
        {
            get => this._progressValue;
            set => this.SetProperty(ref this._progressValue, value);
        }

        /// <summary>
        /// Gets or sets the current status message.
        /// </summary>
        public string StatusMessage
        {
            get => this._statusMessage;
            set => this.SetProperty(ref this._statusMessage, value);
        }

        /// <summary>
        /// Gets or sets a value indicating whether the error message is visible.
        /// </summary>
        public bool IsErrorVisible
        {
            get => this._isErrorVisible;
            set => this.SetProperty(ref this._isErrorVisible, value);
        }

        /// <summary>
        /// Gets the command to close the window.
        /// </summary>
        public ICommand CloseCommand { get; }

        private void Timer_Tick(object? sender, EventArgs e)
        {
            this._step++;

            if (this._step < 20)
            {
                // Initial check
                return;
            }

            if (this._step == 20)
            {
                this.StatusMessage = "Downloading update package...";
            }

            if (this.ProgressValue < 19)
            {
                this.ProgressValue += 0.5;
            }
            else if (this._step > 80)
            {
                // Stall at 19% then fail
                this._timer.Stop();
                this.IsErrorVisible = true;
                this.StatusMessage = "Update failed.";
            }
        }
    }
}
