// <copyright file="ContextMenuService.cs" company="NvidiaControlPanel">
// Copyright (c) NvidiaControlPanel. All rights reserved.
// </copyright>

using System;
using System.Diagnostics;
using System.Security.Principal;
using Microsoft.Win32;

namespace NvidiaControlPanel.Services
{
    /// <summary>
    /// Implementation of the desktop context menu service.
    /// </summary>
    public class ContextMenuService : IContextMenuService
    {
        private const string RegistryPath = @"DesktopBackground\Shell\NvidiaControlPanel";
        private const string MenuText = "NVIDIA Control Panel";

        /// <inheritdoc/>
        public bool IsEnabled()
        {
            try
            {
                using (RegistryKey? key = Registry.ClassesRoot.OpenSubKey(RegistryPath))
                {
                    return key != null;
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
            if (!IsElevated())
            {
                return ElevateAndApply("--enable-context-menu");
            }

            try
            {
                using (RegistryKey key = Registry.ClassesRoot.CreateSubKey(RegistryPath, true))
                {
                    key.SetValue(string.Empty, MenuText);
                    string? exePath = Process.GetCurrentProcess().MainModule?.FileName;
                    if (!string.IsNullOrEmpty(exePath))
                    {
                        key.SetValue("Icon", exePath);
                        using (RegistryKey commandKey = key.CreateSubKey("command"))
                        {
                            commandKey.SetValue(string.Empty, $"\"{exePath}\"");
                        }
                    }
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
            if (!IsElevated())
            {
                return ElevateAndApply("--disable-context-menu");
            }

            try
            {
                Registry.ClassesRoot.DeleteSubKeyTree(RegistryPath, false);
                return true;
            }
            catch
            {
                return false;
            }
        }

        private static bool ElevateAndApply(string arg)
        {
            ProcessStartInfo startInfo = new ProcessStartInfo
            {
                FileName = Process.GetCurrentProcess().MainModule?.FileName,
                UseShellExecute = true,
                Verb = "runas",
                Arguments = arg,
            };

            try
            {
                Process? process = Process.Start(startInfo);
                process?.WaitForExit();
                return process?.ExitCode == 0;
            }
            catch
            {
                return false;
            }
        }

        private static bool IsElevated()
        {
            using (WindowsIdentity identity = WindowsIdentity.GetCurrent())
            {
                WindowsPrincipal principal = new WindowsPrincipal(identity);
                return principal.IsInRole(WindowsBuiltInRole.Administrator);
            }
        }
    }
}
