// <copyright file="SimulationServiceTests.cs" company="NvidiaControlPanel">
// Copyright (c) NvidiaControlPanel. All rights reserved.
// </copyright>

using System;
using System.IO;
using System.Text.Json;
using System.Threading.Tasks;
using NvidiaControlPanel.Services;
using Xunit;

namespace NvidiaControlPanel.Tests
{
    public class SimulationServiceTests
    {
        [Fact]
        public async Task GetConfigAsync_ShouldCreateDefaultFile_WhenMissing()
        {
            // Arrange
            string testDir = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "test_missing_" + Guid.NewGuid());
            var service = new SimulationService(testDir);
            string configPath = Path.Combine(testDir, "gpu_config.json");

            try
            {
                // Act
                var config = await service.GetConfigAsync();

                // Assert
                Assert.True(File.Exists(configPath));
                Assert.Equal("NVIDIA GeForce GTX 1650", config.GpuName);
            }
            finally
            {
                Cleanup(testDir);
            }
        }

        [Fact]
        public async Task GetConfigAsync_ShouldReturnDataFromFile_WhenExists()
        {
            // Arrange
            string testDir = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "test_exists_" + Guid.NewGuid());
            Directory.CreateDirectory(testDir);
            string configPath = Path.Combine(testDir, "gpu_config.json");

            var customConfig = new SimulationConfig
            {
                GpuName = "RTX 4090 Custom",
                DriverVersion = "999.99",
                VideoMemory = "24 GB"
            };
            string json = JsonSerializer.Serialize(customConfig);
            File.WriteAllText(configPath, json);

            var service = new SimulationService(testDir);

            try
            {
                // Act
                var config = await service.GetConfigAsync();

                // Assert
                Assert.Equal("RTX 4090 Custom", config.GpuName);
                Assert.Equal("999.99", config.DriverVersion);
                Assert.Equal("24 GB", config.VideoMemory);
            }
            finally
            {
                Cleanup(testDir);
            }
        }

        [Fact]
        public async Task SaveConfigAsync_ShouldPersistDataToFile()
        {
            // Arrange
            string testDir = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "test_save_" + Guid.NewGuid());
            var service = new SimulationService(testDir);
            string configPath = Path.Combine(testDir, "gpu_config.json");

            var newConfig = new SimulationConfig
            {
                GpuName = "Saved GPU",
                SelectedResolution = "3840 x 2160",
                SelectedRefreshRate = 60
            };

            try
            {
                // Act
                await service.SaveConfigAsync(newConfig);

                // Assert
                Assert.True(File.Exists(configPath));
                string json = File.ReadAllText(configPath);
                var savedConfig = JsonSerializer.Deserialize<SimulationConfig>(json);
                Assert.NotNull(savedConfig);
                Assert.Equal("Saved GPU", savedConfig.GpuName);
                Assert.Equal("3840 x 2160", savedConfig.SelectedResolution);
                Assert.Equal(60, savedConfig.SelectedRefreshRate);
            }
            finally
            {
                Cleanup(testDir);
            }
        }

        private static void Cleanup(string dir)
        {
            if (Directory.Exists(dir))
            {
                Directory.Delete(dir, true);
            }
        }
    }
}