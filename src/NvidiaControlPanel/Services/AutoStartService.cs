// <copyright file="AutoStartService.cs" company="NvidiaControlPanel">
// Copyright (c) NvidiaControlPanel. All rights reserved.
// </copyright>

using System;
using System.Diagnostics;
using Microsoft.Win32;

namespace NvidiaControlPanel.Services
{
    /// <summary>
    /// Implementation of the auto-start service using Windows Registry.
    /// </summary>
    public class AutoStartService : IAutoStartService
    {
        private const string RunKeyPath = @"Software\Microsoft\Windows\CurrentVersion\Run";
        private const string AppName = "NvidiaControlPanelSimulation";

        /// <inheritdoc/>
        public bool IsEnabled()
        {
            try
            {
                using (RegistryKey? key = Registry.CurrentUser.OpenSubKey(RunKeyPath, false))
                {
                    return key?.GetValue(AppName) != null;
                }
            }
            catch
            {
                return false;
            }
        }

        /// <inheritdoc/>
        public bool Enable()
        {
            try
            {
                string? exePath = Process.GetCurrentProcess().MainModule?.FileName;
                if (string.IsNullOrEmpty(exePath))
                {
                    return false;
                }

                // Add --silent flag for stealth launch to tray
                string command = $"\"{exePath}\" --silent";

                using (RegistryKey? key = Registry.CurrentUser.OpenSubKey(RunKeyPath, true))
                {
                    key?.SetValue(AppName, command);
                }

                return true;
            }
            catch
            {
                return false;
            }
        }

        /// <inheritdoc/>
        public bool Disable()
        {
            try
            {
                using (RegistryKey? key = Registry.CurrentUser.OpenSubKey(RunKeyPath, true))
                {
                    key?.DeleteValue(AppName, false);
                }

                return true;
            }
            catch
            {
                return false;
            }
        }
    }
}
