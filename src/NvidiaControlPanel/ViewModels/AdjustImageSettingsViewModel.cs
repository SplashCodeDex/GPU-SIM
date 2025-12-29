using NvidiaControlPanel.ViewModels.Core;

namespace NvidiaControlPanel.ViewModels
{
    /// <summary>
    /// ViewModel for the Adjust Image Settings with Preview page.
    /// </summary>
    public class AdjustImageSettingsViewModel : ViewModelBase
    {
        private bool _isPerformanceSelected;
        private bool _isBalancedSelected = true;
        private bool _isQualitySelected;
        private bool _useAdvancedSettings;
        private bool _useMyPreference = true;

        /// <summary>
        /// Gets or sets a value indicating whether Performance is selected.
        /// </summary>
        public bool IsPerformanceSelected
        {
            get => this._isPerformanceSelected;
            set => this.SetProperty(ref this._isPerformanceSelected, value);
        }

        /// <summary>
        /// Gets or sets a value indicating whether Balanced is selected.
        /// </summary>
        public bool IsBalancedSelected
        {
            get => this._isBalancedSelected;
            set => this.SetProperty(ref this._isBalancedSelected, value);
        }

        /// <summary>
        /// Gets or sets a value indicating whether Quality is selected.
        /// </summary>
        public bool IsQualitySelected
        {
            get => this._isQualitySelected;
            set => this.SetProperty(ref this._isQualitySelected, value);
        }

        /// <summary>
        /// Gets or sets a value indicating whether to use advanced 3D image settings.
        /// </summary>
        public bool UseAdvancedSettings
        {
            get => this._useAdvancedSettings;
            set => this.SetProperty(ref this._useAdvancedSettings, value);
        }

        /// <summary>
        /// Gets or sets a value indicating whether to use user preferences.
        /// </summary>
        public bool UseMyPreference
        {
            get => this._useMyPreference;
            set => this.SetProperty(ref this._useMyPreference, value);
        }
    }
}
