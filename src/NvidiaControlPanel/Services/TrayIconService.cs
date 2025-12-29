// <copyright file="TrayIconService.cs" company="NvidiaControlPanel">
// Copyright (c) NvidiaControlPanel. All rights reserved.
// </copyright>

using System;
using System.Drawing;
using System.Reflection;
using System.Windows;
using System.Windows.Forms;
using Application = System.Windows.Application;

namespace NvidiaControlPanel.Services
{
    /// <summary>
    /// Implementation of the system tray notification icon service.
    /// </summary>
    public sealed class TrayIconService : ITrayIconService, IDisposable
    {
        private readonly NotifyIcon _notifyIcon;
        private bool _disposed;

        /// <summary>
        /// Initializes a new instance of the <see cref="TrayIconService"/> class.
        /// </summary>
        public TrayIconService()
        {
            this._notifyIcon = new NotifyIcon();

            // Try to load the icon from the application resources
            try
            {
                var iconStream = Application.GetResourceStream(new Uri("pack://application:,,,/icon.ico"))?.Stream;
                if (iconStream != null)
                {
                    this._notifyIcon.Icon = new Icon(iconStream);
                }
            }
            catch
            {
                // Fallback to a standard icon if the custom one fails to load
                this._notifyIcon.Icon = SystemIcons.Application;
            }

            this._notifyIcon.Text = "NVIDIA Settings";
            this._notifyIcon.DoubleClick += this.OnTrayIconDoubleClick;

            this.InitializeContextMenu();
        }

        /// <inheritdoc/>
        public void Show()
        {
            this._notifyIcon.Visible = true;
        }

        /// <inheritdoc/>
        public void Hide()
        {
            this._notifyIcon.Visible = false;
        }

        /// <inheritdoc/>
        public void SetVisibility(bool visible)
        {
            this._notifyIcon.Visible = visible;
        }

        /// <inheritdoc/>
        public void Dispose()
        {
            if (!this._disposed)
            {
                this._notifyIcon.Dispose();
                this._disposed = true;
            }
        }

        private static void RestoreMainWindow()
        {
            var mainWindow = Application.Current.MainWindow;
            if (mainWindow != null)
            {
                if (mainWindow.WindowState == WindowState.Minimized)
                {
                    mainWindow.WindowState = WindowState.Normal;
                }

                mainWindow.Show();
                mainWindow.Activate();
            }
        }

        private void InitializeContextMenu()
        {
            var contextMenu = new ContextMenuStrip();

            var openItem = new ToolStripMenuItem("NVIDIA Control Panel");
            openItem.Click += (s, e) => RestoreMainWindow();
            openItem.Font = new System.Drawing.Font(openItem.Font, System.Drawing.FontStyle.Bold);

            var exitItem = new ToolStripMenuItem("Exit");
            exitItem.Click += (s, e) => Application.Current.Shutdown();

            contextMenu.Items.Add(openItem);
            contextMenu.Items.Add(new ToolStripSeparator());
            contextMenu.Items.Add(exitItem);

            this._notifyIcon.ContextMenuStrip = contextMenu;
        }

        private void OnTrayIconDoubleClick(object? sender, EventArgs e)
        {
            RestoreMainWindow();
        }
    }
}