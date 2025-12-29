// <copyright file="JsonSettingsService.cs" company="NvidiaControlPanel">
// Copyright (c) NvidiaControlPanel. All rights reserved.
// </copyright>

using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.IO;
using System.Text.Json;
using NvidiaControlPanel.Models;

namespace NvidiaControlPanel.Services
{
    /// <summary>
    /// File-based implementation of settings service using JSON.
    /// </summary>
    public class JsonSettingsService : ISettingsService
    {
        private const string SettingsFileName = "settings.json";

        private static readonly JsonSerializerOptions SerializerOptions = new JsonSerializerOptions
        {
            WriteIndented = true,
        };

        private readonly string _filePath;

        /// <summary>
        /// Initializes a new instance of the <see cref="JsonSettingsService"/> class.
        /// </summary>
        public JsonSettingsService()
        {
            this._filePath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, SettingsFileName);
        }

        /// <inheritdoc/>
        public Collection<FeatureSetting> Load3DSettings()
        {
            if (!File.Exists(this._filePath))
            {
                return new Collection<FeatureSetting>();
            }

            try
            {
                string json = File.ReadAllText(this._filePath);
                var settings = JsonSerializer.Deserialize<Collection<FeatureSetting>>(json);
                return settings ?? new Collection<FeatureSetting>();
            }
            catch
            {
                // In case of corruption, return empty to fall back to defaults
                return new Collection<FeatureSetting>();
            }
        }

        /// <inheritdoc/>
        public void Save3DSettings(IEnumerable<FeatureSetting> settings)
        {
            try
            {
                string json = JsonSerializer.Serialize(settings, SerializerOptions);
                File.WriteAllText(this._filePath, json);
            }
            catch (Exception)
            {
                // Handle or log error
            }
        }

        /// <inheritdoc/>
        public Collection<string> GetAvailablePrograms()
        {
            return new Collection<string>
            {
                "3D Builder",
                "Adobe Photoshop",
                "Google Chrome",
                "Microsoft Edge",
                "VLC Media Player",
            };
        }
    }
}
