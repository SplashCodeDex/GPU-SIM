// <copyright file="DoubleToDurationConverter.cs" company="NvidiaControlPanel">
// Copyright (c) NvidiaControlPanel. All rights reserved.
// </copyright>

using System;
using System.Globalization;
using System.Windows;
using System.Windows.Data;

namespace NvidiaControlPanel.Converters
{
    /// <summary>
    /// Converts a double value (seconds) to a Duration.
    /// </summary>
    public class DoubleToDurationConverter : IValueConverter
    {
        /// <inheritdoc/>
        public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
        {
            if (value is double seconds)
            {
                return new Duration(TimeSpan.FromSeconds(seconds));
            }

            return new Duration(TimeSpan.FromSeconds(10));
        }

        /// <inheritdoc/>
        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }
}
