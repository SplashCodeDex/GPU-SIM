using System;
using System.Windows;
using NvidiaControlPanel.Services;
using NvidiaControlPanel.ViewModels;

namespace NvidiaControlPanel.Views
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml.
    /// </summary>
    public partial class MainWindow : Window
    {
        /// <summary>
        /// Initializes a new instance of the <see cref="MainWindow"/> class.
        /// </summary>
        [System.Diagnostics.CodeAnalysis.SuppressMessage("Reliability", "CA2000:Dispose objects before losing scope", Justification = "Service lifecycle is managed by the application.")]
        public MainWindow()
        {
            this.InitializeComponent();
            this.DataContext = new MainViewModel(new ContextMenuService(), new SystemInfoService(), new TrayIconService());
        }

        /// <inheritdoc/>
        protected override void OnClosing(System.ComponentModel.CancelEventArgs e)
        {
            ArgumentNullException.ThrowIfNull(e);

            // Instead of closing, hide the window to the tray
            e.Cancel = true;
            this.Hide();

            base.OnClosing(e);
        }
    }
}
