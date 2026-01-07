using Moq;
using NvidiaControlPanel.Models;
using NvidiaControlPanel.Services;
using NvidiaControlPanel.ViewModels;
using System.Collections.ObjectModel;
using Xunit;

namespace NvidiaControlPanel.Tests
{
    public class Manage3DSettingsViewModelTests
    {
        [Fact]
        public void Constructor_Initialization_ShouldLoadSettingsAndPrograms()
        {
            // Arrange
            var mockSettingsService = new Mock<ISettingsService>();
            var expectedSettings = new Collection<FeatureSetting>
            {
                new FeatureSetting { Name = "Ambient Occlusion", Value = "Performance" }
            };
            var expectedPrograms = new Collection<string> { "Program1", "Program2" };

            mockSettingsService.Setup(s => s.Load3DSettings()).Returns(expectedSettings);
            mockSettingsService.Setup(s => s.GetAvailablePrograms()).Returns(expectedPrograms);

            var gpuInfo = new GpuInformation { GpuName = "Test GPU" };

            // Act
            var viewModel = new Manage3DSettingsViewModel(mockSettingsService.Object, gpuInfo);

            // Assert
            var setting = viewModel.Settings.FirstOrDefault(s => s.Name == "Ambient Occlusion");
            Assert.NotNull(setting);
            Assert.Equal("Performance", setting.Value);
            Assert.Equal(2, viewModel.Programs.Count);
            Assert.Equal("Program1", viewModel.SelectedProgram);
        }

        [Fact]
        public void RestoreDefaults_ShouldUseDynamicGpuName()
        {
            // Arrange
            var mockSettingsService = new Mock<ISettingsService>();
            mockSettingsService.Setup(s => s.Load3DSettings()).Returns(new Collection<FeatureSetting>());
            mockSettingsService.Setup(s => s.GetAvailablePrograms()).Returns(new Collection<string>());

            var gpuInfo = new GpuInformation { GpuName = "Dynamic Test GPU" };
            var viewModel = new Manage3DSettingsViewModel(mockSettingsService.Object, gpuInfo);

            // Act
            viewModel.RestoreDefaultsCommand.Execute(null);

            // Assert
            var openGlSetting = viewModel.Settings.FirstOrDefault(s => s.Name == "OpenGL rendering GPU");
            Assert.NotNull(openGlSetting);
            Assert.Contains("Dynamic Test GPU", openGlSetting.Options);
        }
    }
}
