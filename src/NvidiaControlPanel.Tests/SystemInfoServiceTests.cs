using Moq;
using NvidiaControlPanel.Services;
using Xunit;

namespace NvidiaControlPanel.Tests
{
    public class SystemInfoServiceTests
    {
        [Fact]
        public async Task GetGpuInformation_ShouldReturnDataFromSimulationService()
        {
            // Arrange
            var mockSimulation = new Mock<ISimulationService>();
            var expectedConfig = new SimulationConfig
            {
                GpuName = "Test GPU",
                DriverVersion = "Test Driver",
                VideoMemory = "Test Memory",
                BusSupport = "Test Bus",
                BiosVersion = "Test BIOS",
                DirectXSupport = "Test DX",
                DeviceId = "Test ID",
                VendorId = "Test Vendor"
            };

            mockSimulation.Setup(s => s.GetConfigAsync()).ReturnsAsync(expectedConfig);

            var service = new SystemInfoService(mockSimulation.Object);

            // Act
            var info = await service.GetGpuInformationAsync();

            // Assert
            Assert.Equal("Test GPU", info.GpuName);
            Assert.Equal("Test Driver", info.DriverVersion);
            Assert.Equal("Test Memory", info.VideoMemory);
            Assert.Equal("Test Bus", info.BusSupport);
            Assert.Equal("Test BIOS", info.BiosVersion);
            Assert.Equal("Test DX", info.DirectXSupport);
            Assert.Equal("Test ID", info.DeviceId);
            Assert.Equal("Test Vendor", info.VendorId);
        }
    }
}
