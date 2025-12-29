// <copyright file="FakeUpdateView.xaml.cs" company="NvidiaControlPanel">
// Copyright (c) NvidiaControlPanel. All rights reserved.
// </copyright>

using System.Windows;
using NvidiaControlPanel.ViewModels;

namespace NvidiaControlPanel.Views
{
    /// <summary>
    /// Interaction logic for FakeUpdateView.xaml.
    /// </summary>
    public partial class FakeUpdateView : Window
    {
        /// <summary>
        /// Initializes a new instance of the <see cref="FakeUpdateView"/> class.
        /// </summary>
        public FakeUpdateView()
        {
            this.InitializeComponent();
            this.DataContext = new FakeUpdateViewModel();
        }
    }
}
