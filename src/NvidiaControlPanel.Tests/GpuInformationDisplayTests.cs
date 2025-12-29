using NvidiaControlPanel.Models;
using Xunit;

namespace NvidiaControlPanel.Tests
{
    public class GpuInformationDisplayTests
    {
        [Fact]
        public void GpuInformation_ShouldHoldDisplaySettings()
        {
            // Arrange
            var info = new GpuInformation
            {
                SelectedResolution = "2560 x 1440",
                SelectedRefreshRate = 144
            };

            // Assert
            Assert.Equal("2560 x 1440", info.SelectedResolution);
            Assert.Equal(144, info.SelectedRefreshRate);
        }
    }
}
