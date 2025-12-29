using NvidiaControlPanel.Services;
using NvidiaControlPanel.ViewModels;
using Xunit;
using Moq;

namespace NvidiaControlPanel.Tests
{
    public class MainViewModelTests
    {
        [Fact]
        public async Task Constructor_ShouldInitializeGpuNameFromService()
        {
            // Arrange
            var mockContextMenu = new Mock<IContextMenuService>();
            var mockSystemInfo = new Mock<ISystemInfoService>();
            var mockTrayIcon = new Mock<ITrayIconService>();
            var mockAutoStart = new Mock<IAutoStartService>();
            var tcs = new TaskCompletionSource<Models.GpuInformation>();

            mockSystemInfo.Setup(s => s.GetGpuInformationAsync()).ReturnsAsync(new Models.GpuInformation
            {
                GpuName = "Test GPU",
                DriverVersion = "1.2.3",
                VideoMemory = "1 GB"
            });

            // Act
            var viewModel = new MainViewModel(mockContextMenu.Object, mockSystemInfo.Object, mockTrayIcon.Object, mockAutoStart.Object);

            // Wait for async init (poor man's sync for fire-and-forget)
            // Ideally MainViewModel should expose a Task or IsInitialized property
            await Task.Delay(100);

            // Assert
            Assert.Equal("System Information: Test GPU", viewModel.StatusBarText);
        }
    }
}
