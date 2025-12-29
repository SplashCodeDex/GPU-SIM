// <copyright file="ConfirmationDialogView.xaml.cs" company="NvidiaControlPanel">
// Copyright (c) NvidiaControlPanel. All rights reserved.
// </copyright>

using System;
using System.Windows;
using System.Windows.Threading;

namespace NvidiaControlPanel.Views
{
    /// <summary>
    /// Interaction logic for ConfirmationDialogView.xaml.
    /// </summary>
    public partial class ConfirmationDialogView : Window
    {
        private readonly DispatcherTimer _timer;
        private int _secondsRemaining;

        /// <summary>
        /// Initializes a new instance of the <see cref="ConfirmationDialogView"/> class.
        /// </summary>
        /// <param name="timeoutSeconds">The countdown duration.</param>
        public ConfirmationDialogView(int timeoutSeconds)
        {
            this.InitializeComponent();
            this._secondsRemaining = timeoutSeconds;
            this.Result = false;

            this._timer = new DispatcherTimer();
            this._timer.Interval = TimeSpan.FromSeconds(1);
            this._timer.Tick += this.Timer_Tick;
            this._timer.Start();

            this.UpdateTimerText();
        }

        /// <summary>
        /// Gets a value indicating whether the user confirmed.
        /// </summary>
        public bool Result { get; private set; }

        private void Timer_Tick(object? sender, EventArgs e)
        {
            this._secondsRemaining--;
            if (this._secondsRemaining <= 0)
            {
                this._timer.Stop();
                this.Close();
            }
            else
            {
                this.UpdateTimerText();
            }
        }

        private void UpdateTimerText()
        {
            this.TimerText.Text = $"Reverting in {this._secondsRemaining} seconds";
        }

        private void YesButton_Click(object sender, RoutedEventArgs e)
        {
            this.Result = true;
            this._timer.Stop();
            this.DialogResult = true;
            this.Close();
        }

        private void NoButton_Click(object sender, RoutedEventArgs e)
        {
            this.Result = false;
            this._timer.Stop();
            this.DialogResult = false;
            this.Close();
        }
    }
}
