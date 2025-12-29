using NvidiaControlPanel.Services;
using NvidiaControlPanel.ViewModels;
using Xunit;
using Moq;

namespace NvidiaControlPanel.Tests
{
    public class MainViewModelTests
    {
        [Fact]
        public void Constructor_ShouldInitializeGpuNameFromService()
        {
            // Arrange
            var mockRegistry = new Mock<IRegistryService>();
            var mockSystemInfo = new Mock<ISystemInfoService>();
            mockSystemInfo.Setup(s => s.GetGpuInformation()).Returns(new Models.GpuInformation
            {
                GpuName = "Test GPU",
                DriverVersion = "1.2.3",
                VideoMemory = "1 GB"
            });

            // Act
            var viewModel = new MainViewModel(mockRegistry.Object, mockSystemInfo.Object);

            // Assert
            Assert.Equal("System Information: Test GPU", viewModel.StatusBarText);
        }
    }
}
