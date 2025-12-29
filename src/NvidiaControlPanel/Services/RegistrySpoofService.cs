// <copyright file="RegistrySpoofService.cs" company="NvidiaControlPanel">
// Copyright (c) NvidiaControlPanel. All rights reserved.
// </copyright>

using System;
using System.Diagnostics;
using System.Security.Principal;
using Microsoft.Win32;
using NvidiaControlPanel.Models;

namespace NvidiaControlPanel.Services
{
    /// <summary>
    /// Service for applying GPU information to the Windows Registry.
    /// </summary>
    public class RegistrySpoofService : IRegistrySpoofService
    {
        private const string DisplayClassGuid = "{4d36e968-e325-11ce-bfc1-08002be10318}";
        private const string BaseRegistryPath = @"SYSTEM\CurrentControlSet\Control\Class\" + DisplayClassGuid;

        /// <inheritdoc/>
        public bool IsElevated()
        {
            using (WindowsIdentity identity = WindowsIdentity.GetCurrent())
            {
                WindowsPrincipal principal = new WindowsPrincipal(identity);
                return principal.IsInRole(WindowsBuiltInRole.Administrator);
            }
        }

        /// <inheritdoc/>
        public bool ApplySpoof(GpuInformation info)
        {
            ArgumentNullException.ThrowIfNull(info);

            if (!this.IsElevated())
            {
                return ElevateAndApply();
            }

            try
            {
                using (RegistryKey? baseKey = Registry.LocalMachine.OpenSubKey(BaseRegistryPath, true))
                {
                    if (baseKey == null)
                    {
                        return false;
                    }

                    foreach (string subKeyName in baseKey.GetSubKeyNames())
                    {
                        // Match 0000, 0001, etc.
                        if (subKeyName.Length == 4 && int.TryParse(subKeyName, out _))
                        {
                            using (RegistryKey? adapterKey = baseKey.OpenSubKey(subKeyName, true))
                            {
                                if (adapterKey != null)
                                {
                                    // Update Name
                                    adapterKey.SetValue("HardwareInformation.AdapterString", info.GpuName, RegistryValueKind.String);

                                    // Update VRAM (Simulated as 4GB for now in memory size format if needed)
                                    // Windows uses qwMemorySize for 64-bit systems
                                    if (ulong.TryParse(info.VideoMemory.Split(' ')[0], out ulong memoryGb))
                                    {
                                        ulong bytes = memoryGb * 1024 * 1024 * 1024;
                                        adapterKey.SetValue("HardwareInformation.qwMemorySize", (long)bytes, RegistryValueKind.QWord);
                                        adapterKey.SetValue("HardwareInformation.MemorySize", (int)bytes, RegistryValueKind.DWord);
                                    }
                                }
                            }
                        }
                    }
                }

                return true;
            }
            catch (Exception)
            {
                return false;
            }
        }

        private static bool ElevateAndApply()
        {
            ProcessStartInfo startInfo = new ProcessStartInfo
            {
                FileName = Process.GetCurrentProcess().MainModule?.FileName,
                UseShellExecute = true,
                Verb = "runas",
                Arguments = "--apply-spoof", // Hidden arg for child process to handle
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
    }
}
