// <copyright file="NavigationServiceTests.cs" company="NvidiaControlPanel">
// Copyright (c) NvidiaControlPanel. All rights reserved.
// </copyright>

using NvidiaControlPanel.Services;
using Xunit;

namespace NvidiaControlPanel.Tests
{
    public class NavigationServiceTests
    {
        [Fact]
        public void InitialState_ShouldHaveNoHistory()
        {
            var service = new NavigationService();

            Assert.False(service.CanGoBack);
            Assert.False(service.CanGoForward);
            Assert.Null(service.PreviousViewName);
            Assert.Null(service.NextViewName);
        }

        [Fact]
        public void RecordNavigation_ShouldEnableGoBack()
        {
            var service = new NavigationService();

            service.RecordNavigation("Manage3DSettings");
            service.RecordNavigation("ChangeResolution");

            Assert.True(service.CanGoBack);
            Assert.False(service.CanGoForward);
            Assert.Equal("Manage 3D settings", service.PreviousViewName);
        }

        [Fact]
        public void RecordNavigation_Home_ShouldNotBeAddedToHistory()
        {
            var service = new NavigationService();

            service.RecordNavigation("Home");
            
            Assert.False(service.CanGoBack);
            Assert.Null(service.PreviousViewName);
        }

        [Fact]
        public void GoBack_ShouldReturnPreviousViewAndEnableGoForward()
        {
            var service = new NavigationService();
            service.RecordNavigation("Manage3DSettings");
            service.RecordNavigation("ChangeResolution");

            var result = service.GoBack();

            Assert.Equal("Manage3DSettings", result);
            Assert.False(service.CanGoBack);
            Assert.True(service.CanGoForward);
            Assert.Equal("Change resolution", service.NextViewName);
        }

        [Fact]
        public void GoForward_ShouldReturnNextView()
        {
            var service = new NavigationService();
            service.RecordNavigation("Manage3DSettings");
            service.RecordNavigation("ChangeResolution");
            service.GoBack();

            var result = service.GoForward();

            Assert.Equal("ChangeResolution", result);
            Assert.True(service.CanGoBack);
            Assert.False(service.CanGoForward);
        }

        [Fact]
        public void NewNavigation_ShouldClearForwardStack()
        {
            var service = new NavigationService();
            service.RecordNavigation("Manage3DSettings");
            service.RecordNavigation("ChangeResolution");
            service.GoBack();
            
            service.RecordNavigation("AdjustImageSettings");

            Assert.False(service.CanGoForward);
            Assert.Null(service.NextViewName);
            Assert.True(service.CanGoBack);
            Assert.Equal("Manage 3D settings", service.PreviousViewName);
        }

        [Fact]
        public void DuplicateNavigation_ShouldNotAddSameConsecutiveView()
        {
            var service = new NavigationService();
            service.RecordNavigation("Manage3DSettings");
            service.RecordNavigation("Manage3DSettings");

            Assert.False(service.CanGoBack);
        }
    }
}
