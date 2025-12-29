using NvidiaControlPanel.Services;
using Xunit;

namespace NvidiaControlPanel.Tests
{
    public class SystemInfoServiceTests
    {
        [Fact]
        public void GetGpuInformation_ShouldReturnSpoofedData()
        {
            // Arrange
            var service = new SystemInfoService();

            // Act
            var info = service.GetGpuInformation();

            // Assert
            Assert.Equal("NVIDIA GeForce GTX 1650", info.GpuName);
            Assert.Equal("560.94", info.DriverVersion);
            Assert.Equal("4096 MB GDDR5", info.VideoMemory);
        }
    }
}
