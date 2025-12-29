using NvidiaControlPanel.ViewModels;
using Xunit;

namespace NvidiaControlPanel.Tests
{
    public class AdjustImageSettingsViewModelTests
    {
        [Fact]
        public void PropertyChange_ShouldUpdateState()
        {
            // Arrange
            var viewModel = new AdjustImageSettingsViewModel();

            // Act
            viewModel.IsPerformanceSelected = true;
            viewModel.IsBalancedSelected = false;

            // Assert
            Assert.True(viewModel.IsPerformanceSelected);
            Assert.False(viewModel.IsBalancedSelected);
        }

        [Fact]
        public void Defaults_ShouldBeCorrect()
        {
            // Arrange & Act
            var viewModel = new AdjustImageSettingsViewModel();

            // Assert
            Assert.True(viewModel.IsBalancedSelected);
            Assert.False(viewModel.IsPerformanceSelected);
            Assert.False(viewModel.IsQualitySelected);
            Assert.True(viewModel.UseMyPreference);
        }

        [Fact]
        public void Slider_ShouldSyncWithRadioButtons()
        {
            // Arrange
            var viewModel = new AdjustImageSettingsViewModel();

            // Act: Change Slider to Performance (0)
            viewModel.PreferenceValue = 0;
            // Assert
            Assert.True(viewModel.IsPerformanceSelected);
            Assert.False(viewModel.IsBalancedSelected);
            Assert.False(viewModel.IsQualitySelected);

            // Act: Change Radio to Quality
            viewModel.IsQualitySelected = true;
            // Assert
            Assert.Equal(2, viewModel.PreferenceValue);
            Assert.False(viewModel.IsPerformanceSelected);
            Assert.False(viewModel.IsBalancedSelected);
        }
    }
}
