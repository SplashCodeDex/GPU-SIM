using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Runtime.CompilerServices;

namespace NvidiaControlPanel.Models
{
    /// <summary>
    /// Represents a single 3D setting feature.
    /// </summary>
    public class FeatureSetting : INotifyPropertyChanged
    {
        private string _value = string.Empty;
        private bool _isModified;

        /// <inheritdoc/>
        public event PropertyChangedEventHandler? PropertyChanged;

        /// <summary>
        /// Gets or sets the name of the feature.
        /// </summary>
        public string Name { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the current value of the feature.
        /// </summary>
        public string Value
        {
            get => this._value;
            set
            {
                if (this._value != value)
                {
                    this._value = value;
                    this.OnPropertyChanged();
                    this.IsModified = this._value != this.DefaultValue;
                }
            }
        }

        /// <summary>
        /// Gets or sets the default value for this setting.
        /// </summary>
        public string DefaultValue { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets a value indicating whether the setting has been modified from default.
        /// </summary>
        public bool IsModified
        {
            get => this._isModified;
            set
            {
                if (this._isModified != value)
                {
                    this._isModified = value;
                    this.OnPropertyChanged();
                }
            }
        }

        /// <summary>
        /// Gets the available options for the feature.
        /// </summary>
        public Collection<string> Options { get; } = new Collection<string>();

        /// <summary>
        /// Gets or sets a value indicating whether this is a global setting.
        /// </summary>
        public bool IsGlobal { get; set; }

        /// <summary>
        /// Raises the <see cref="PropertyChanged"/> event.
        /// </summary>
        /// <param name="propertyName">The name of the property that changed.</param>
        protected void OnPropertyChanged([CallerMemberName] string? propertyName = null)
        {
            this.PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }
}
