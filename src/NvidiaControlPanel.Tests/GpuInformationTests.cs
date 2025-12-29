using NvidiaControlPanel.Models;
using Xunit;

namespace NvidiaControlPanel.Tests
{
    public class GpuInformationTests
    {
        [Fact]
        public void GpuInformation_ShouldHoldExtendedProperties()
        {
            // Arrange
            var info = new GpuInformation
            {
                BusSupport = "PCI Express x16 Gen 3",
                BiosVersion = "90.06.33.00.70",
                DirectXSupport = "12 Ultimate",
                DeviceId = "1F82",
                VendorId = "10DE"
            };

            // Assert
            Assert.Equal("PCI Express x16 Gen 3", info.BusSupport);
            Assert.Equal("90.06.33.00.70", info.BiosVersion);
            Assert.Equal("12 Ultimate", info.DirectXSupport);
            Assert.Equal("1F82", info.DeviceId);
            Assert.Equal("10DE", info.VendorId);
        }
    }
}
