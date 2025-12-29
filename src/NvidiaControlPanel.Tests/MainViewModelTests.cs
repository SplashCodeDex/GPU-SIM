using NvidiaControlPanel.Services;
using NvidiaControlPanel.ViewModels;
using Xunit;
using Moq;

namespace NvidiaControlPanel.Tests
{
    public class MainViewModelTests
    {
        private readonly Mock<IContextMenuService> _mockContextMenu = new();
        private readonly Mock<ISystemInfoService> _mockSystemInfo = new();
        private readonly Mock<ITrayIconService> _mockTrayIcon = new();
        private readonly Mock<IAutoStartService> _mockAutoStart = new();
        private readonly Mock<INavigationService> _mockNavigation = new();

        public MainViewModelTests()
        {
            this._mockSystemInfo.Setup(s => s.GetGpuInformationAsync()).ReturnsAsync(new Models.GpuInformation
            {
                GpuName = "Test GPU",
                DriverVersion = "1.2.3",
                VideoMemory = "1 GB"
            });
        }

        [Fact]
        public async Task Constructor_ShouldInitializeGpuNameFromService()
        {
            // Act
            var viewModel = new MainViewModel(
                this._mockContextMenu.Object,
                this._mockSystemInfo.Object,
                this._mockTrayIcon.Object,
                this._mockAutoStart.Object,
                this._mockNavigation.Object);

            await Task.Delay(100);

            // Assert
            Assert.Equal("System Information: Test GPU", viewModel.StatusBarText);
        }

        [Fact]
        public void BackCommand_ShouldDelegateToNavigationService()
        {
            // Arrange
            this._mockNavigation.Setup(n => n.CanGoBack).Returns(true);
            this._mockNavigation.Setup(n => n.GoBack()).Returns("Manage3DSettings");
            
            var viewModel = new MainViewModel(
                this._mockContextMenu.Object,
                this._mockSystemInfo.Object,
                this._mockTrayIcon.Object,
                this._mockAutoStart.Object,
                this._mockNavigation.Object);

            // Act
            viewModel.BackCommand.Execute(null);

            // Assert
            this._mockNavigation.Verify(n => n.GoBack(), Times.Once);
            Assert.IsType<Manage3DSettingsViewModel>(viewModel.CurrentView);
        }

        [Fact]
        public void ForwardCommand_ShouldDelegateToNavigationService()
        {
            // Arrange
            this._mockNavigation.Setup(n => n.CanGoForward).Returns(true);
            this._mockNavigation.Setup(n => n.GoForward()).Returns("ChangeResolution");
            
            var viewModel = new MainViewModel(
                this._mockContextMenu.Object,
                this._mockSystemInfo.Object,
                this._mockTrayIcon.Object,
                this._mockAutoStart.Object,
                this._mockNavigation.Object);

            // Act
            viewModel.ForwardCommand.Execute(null);

            // Assert
            this._mockNavigation.Verify(n => n.GoForward(), Times.Once);
            Assert.IsType<DisplayResolutionViewModel>(viewModel.CurrentView);
        }

        [Fact]
        public void NavigateCommand_ShouldRecordNavigationInService()
        {
            // Arrange
            var viewModel = new MainViewModel(
                this._mockContextMenu.Object,
                this._mockSystemInfo.Object,
                this._mockTrayIcon.Object,
                this._mockAutoStart.Object,
                this._mockNavigation.Object);

            // Act
            viewModel.NavigateCommand.Execute("Manage3DSettings");

            // Assert
            this._mockNavigation.Verify(n => n.RecordNavigation("Manage3DSettings"), Times.Once);
        }
    }
}
