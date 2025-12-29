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
        public MainWindow()
        {
            this.InitializeComponent();
            this.DataContext = new MainViewModel(new ContextMenuService(), new SystemInfoService());
        }
    }
}
