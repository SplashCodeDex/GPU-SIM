// <copyright file="SimulationService.cs" company="NvidiaControlPanel">
// Copyright (c) NvidiaControlPanel. All rights reserved.
// </copyright>

using System;
using System.IO;
using System.Text.Json;
using System.Threading.Tasks;

namespace NvidiaControlPanel.Services
{
    /// <summary>
    /// Implementation of the simulation service.
    /// </summary>
    public class SimulationService : ISimulationService
    {
        private const string ConfigDirectory = "config";
        private const string ConfigFileName = "gpu_config.json";
        private static readonly string ConfigPath = Path.Combine(ConfigDirectory, ConfigFileName);

        private static readonly JsonSerializerOptions SerializerOptions = new JsonSerializerOptions
        {
            WriteIndented = true,
        };

        private SimulationConfig? _cachedConfig;

        /// <summary>
        /// Retrieves the simulation configuration asynchronously.
        /// </summary>
        /// <returns>The simulation configuration.</returns>
        public async Task<SimulationConfig> GetConfigAsync()
        {
            if (this._cachedConfig != null)
            {
                return this._cachedConfig;
            }

            try
            {
                if (!Directory.Exists(ConfigDirectory))
                {
                    Directory.CreateDirectory(ConfigDirectory);
                }

                if (File.Exists(ConfigPath))
                {
                    string json = await File.ReadAllTextAsync(ConfigPath).ConfigureAwait(false);
                    var config = JsonSerializer.Deserialize<SimulationConfig>(json);
                    this._cachedConfig = config ?? CreateDefaultConfig();
                }
                else
                {
                    this._cachedConfig = CreateDefaultConfig();
                    await this.SaveConfigAsync(this._cachedConfig).ConfigureAwait(false);
                }
            }
            catch (Exception)
            {
                // Fallback on error
                this._cachedConfig = new SimulationConfig();
            }

            return this._cachedConfig;
        }

        /// <summary>
        /// Retrieves the simulation configuration synchronously.
        /// </summary>
        /// <returns>The simulation configuration.</returns>
        public SimulationConfig GetConfig()
        {
            // Sync wrapper for where async isn't possible yet
            return this.GetConfigAsync().GetAwaiter().GetResult();
        }

        /// <inheritdoc/>
        public async Task SaveConfigAsync(SimulationConfig config)
        {
            this._cachedConfig = config;

            if (!Directory.Exists(ConfigDirectory))
            {
                Directory.CreateDirectory(ConfigDirectory);
            }

            string json = JsonSerializer.Serialize(config, SerializerOptions);
            await File.WriteAllTextAsync(ConfigPath, json).ConfigureAwait(false);
        }

        /// <inheritdoc/>
        public void SaveConfig(SimulationConfig config)
        {
            this.SaveConfigAsync(config).GetAwaiter().GetResult();
        }

        private static SimulationConfig CreateDefaultConfig()
        {
            return new SimulationConfig();
        }
    }
}