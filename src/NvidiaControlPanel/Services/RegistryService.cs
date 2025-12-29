using System;
using System.Diagnostics;
using System.Reflection;
using Microsoft.Win32;

namespace NvidiaControlPanel.Services
{
    /// <summary>
    /// Service for interacting with the Windows Registry to manage the Context Menu.
    /// </summary>
    public class RegistryService : IRegistryService
    {
        private const string ContextMenuPath = @"Software\Classes\Directory\Background\shell\NvidiaControlPanel";
        private const string CommandPath = @"Software\Classes\Directory\Background\shell\NvidiaControlPanel\command";

        /// <inheritdoc/>
        public void EnableContextMenu()
        {
            try
            {
                using (RegistryKey key = Registry.CurrentUser.CreateSubKey(ContextMenuPath))
                {
                    key.SetValue(string.Empty, "NVIDIA Control Panel");
                    key.SetValue("Icon", Environment.ProcessPath!);
                }

                using (RegistryKey key = Registry.CurrentUser.CreateSubKey(CommandPath))
                {
                    key.SetValue(string.Empty, $"\"{Environment.ProcessPath}\"");
                }
            }
            catch (Exception ex)
            {
                // In a real app, logging would happen here.
                System.Diagnostics.Debug.WriteLine($"Failed to add context menu: {ex.Message}");
            }
        }

        /// <inheritdoc/>
        public void DisableContextMenu()
        {
            try
            {
                Registry.CurrentUser.DeleteSubKeyTree(ContextMenuPath, false);
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"Failed to remove context menu: {ex.Message}");
            }
        }

        /// <inheritdoc/>
        public bool IsContextMenuEnabled()
        {
             using (RegistryKey? key = Registry.CurrentUser.OpenSubKey(ContextMenuPath))
             {
                 return key != null;
             }
        }
    }
}
