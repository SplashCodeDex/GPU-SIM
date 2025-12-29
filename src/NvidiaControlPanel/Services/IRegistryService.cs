namespace NvidiaControlPanel.Services
{
    /// <summary>
    /// Interface for interacting with the Windows Registry.
    /// </summary>
    public interface IRegistryService
    {
        /// <summary>
        /// Enables the desktop context menu entry.
        /// </summary>
        void EnableContextMenu();

        /// <summary>
        /// Disables the desktop context menu entry.
        /// </summary>
        void DisableContextMenu();

        /// <summary>
        /// Checks if the desktop context menu entry is currently enabled.
        /// </summary>
        /// <returns>True if enabled; otherwise, false.</returns>
        bool IsContextMenuEnabled();
    }
}
