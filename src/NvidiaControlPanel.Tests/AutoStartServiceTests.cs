// <copyright file="AutoStartServiceTests.cs" company="NvidiaControlPanel">
// Copyright (c) NvidiaControlPanel. All rights reserved.
// </copyright>

using NvidiaControlPanel.Services;
using Xunit;

namespace NvidiaControlPanel.Tests
{
    public class AutoStartServiceTests
    {
        [Fact]
        public void AutoStartService_ShouldToggleState()
        {
            // Note: This test might interact with the real registry HKCU.
            // In a real project we might mock the registry, but here we'll test the logic.
            // We use a try-finally to ensure we don't leave the app in startup.
            
            var service = new AutoStartService();
            bool originalState = service.IsEnabled();

            try
            {
                // Act: Enable
                bool enableResult = service.Enable();
                Assert.True(enableResult);
                Assert.True(service.IsEnabled());

                // Act: Disable
                bool disableResult = service.Disable();
                Assert.True(disableResult);
                Assert.False(service.IsEnabled());
            }
            finally
            {
                // Restore
                if (originalState)
                {
                    service.Enable();
                }
                else
                {
                    service.Disable();
                }
            }
        }
    }
}
