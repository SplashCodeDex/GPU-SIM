using NvidiaControlPanel.Models;
using NvidiaControlPanel.ViewModels;
using Xunit;

namespace NvidiaControlPanel.Tests
{
    public class ViewModelExtendedInfoTests
    {
        private readonly GpuInformation _gpuInfo;

        public ViewModelExtendedInfoTests()
        {
            this._gpuInfo = new GpuInformation
            {
                GpuName = "Test GPU",
                DriverVersion = "1.2.3",
                VideoMemory = "1 GB",
                BusSupport = "PCI Express x16 Gen 4",
                BiosVersion = "99.99.99.99.99",
                DirectXSupport = "12.2",
                DeviceId = "ABCD",
                VendorId = "10DE"
            };
        }

        [Fact]
        public void HomeViewModel_ShouldExposeExtendedInfo()
        {
            // Act
            var vm = new HomeViewModel(this._gpuInfo);

            // Assert
            Assert.Equal("Test GPU", vm.GpuName);
            Assert.Equal("1.2.3", vm.DriverVersion);
            Assert.Equal("1 GB", vm.VideoMemory);
            // New fields (will fail to compile initially)
            Assert.Equal("PCI Express x16 Gen 4", vm.BusSupport);
            Assert.Equal("99.99.99.99.99", vm.BiosVersion);
            Assert.Equal("12.2", vm.DirectXSupport);
        }

        [Fact]
        public void SystemInfoViewModel_ShouldExposeExtendedInfo()
        {
            // Act
            var vm = new SystemInfoViewModel(this._gpuInfo);

            // Assert
            Assert.Equal("Test GPU", vm.GpuName);
            Assert.Equal("1.2.3", vm.DriverVersion);
            Assert.Equal("1 GB", vm.VideoMemory);
            // New fields (will fail to compile initially)
            Assert.Equal("PCI Express x16 Gen 4", vm.BusSupport);
            Assert.Equal("99.99.99.99.99", vm.BiosVersion);
            Assert.Equal("12.2", vm.DirectXSupport);
            Assert.Equal("ABCD", vm.DeviceId);
            Assert.Equal("10DE", vm.VendorId);
        }
    }
}
