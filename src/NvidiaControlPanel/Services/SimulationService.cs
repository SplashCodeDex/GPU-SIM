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
        private const string DefaultConfigDirectory = "config";
        private const string ConfigFileName = "gpu_config.json";

        private static readonly JsonSerializerOptions SerializerOptions = new JsonSerializerOptions
        {
            WriteIndented = true,
        };

        private readonly string _configDirectory;
        private readonly string _configPath;
        private SimulationConfig? _cachedConfig;

        /// <summary>
        /// Initializes a new instance of the <see cref="SimulationService"/> class.
        /// </summary>
        public SimulationService()
            : this(DefaultConfigDirectory)
        {
        }

        /// <summary>
        /// Initializes a new instance of the <see cref="SimulationService"/> class with a custom config directory.
        /// </summary>
        /// <param name="configDirectory">The directory to store configuration in.</param>
        public SimulationService(string configDirectory)
        {
            this._configDirectory = configDirectory;
            this._configPath = Path.Combine(configDirectory, ConfigFileName);
        }

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
                if (!Directory.Exists(this._configDirectory))
                {
                    Directory.CreateDirectory(this._configDirectory);
                }

                if (File.Exists(this._configPath))
                {
                    string json = await File.ReadAllTextAsync(this._configPath).ConfigureAwait(false);
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

            if (!Directory.Exists(this._configDirectory))
            {
                Directory.CreateDirectory(this._configDirectory);
            }

            string json = JsonSerializer.Serialize(config, SerializerOptions);
            await File.WriteAllTextAsync(this._configPath, json).ConfigureAwait(false);
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