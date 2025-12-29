using System;
using System.IO;
using System.Text.Json;
using System.Threading.Tasks;
using NvidiaControlPanel.Services;
using Xunit;

namespace NvidiaControlPanel.Tests
{
    public class SimulationServiceTests : IDisposable
    {
        private const string ConfigDirectory = "config";
        private const string ConfigFileName = "gpu_config.json";
        private static readonly string ConfigPath = Path.Combine(ConfigDirectory, ConfigFileName);

        public SimulationServiceTests()
        {
            this.Cleanup();
        }

        public void Dispose()
        {
            this.Cleanup();
        }

        private void Cleanup()
        {
            if (File.Exists(ConfigPath))
            {
                File.Delete(ConfigPath);
            }
            if (Directory.Exists(ConfigDirectory))
            {
                Directory.Delete(ConfigDirectory, true);
            }
        }

        [Fact]
        public async Task GetConfigAsync_ShouldCreateDefaultFile_WhenMissing()
        {
            // Arrange
            var service = new SimulationService();

            // Act
            var config = await service.GetConfigAsync();

            // Assert
            Assert.True(File.Exists(ConfigPath));
            Assert.Equal("NVIDIA GeForce GTX 1650", config.GpuName);
            
            // Verify file content
            string json = File.ReadAllText(ConfigPath);
            var savedConfig = JsonSerializer.Deserialize<SimulationConfig>(json);
            Assert.NotNull(savedConfig);
            Assert.Equal("NVIDIA GeForce GTX 1650", savedConfig.GpuName);
        }

        [Fact]
        public async Task GetConfigAsync_ShouldReturnDataFromFile_WhenExists()
        {
            // Arrange
            if (!Directory.Exists(ConfigDirectory))
            {
                Directory.CreateDirectory(ConfigDirectory);
            }

            var customConfig = new SimulationConfig
            {
                GpuName = "RTX 4090 Custom",
                DriverVersion = "999.99",
                VideoMemory = "24 GB"
            };
            string json = JsonSerializer.Serialize(customConfig);
            File.WriteAllText(ConfigPath, json);

            var service = new SimulationService();

            // Act
            var config = await service.GetConfigAsync();

            // Assert
            Assert.Equal("RTX 4090 Custom", config.GpuName);
            Assert.Equal("999.99", config.DriverVersion);
            Assert.Equal("24 GB", config.VideoMemory);
        }
    }
}