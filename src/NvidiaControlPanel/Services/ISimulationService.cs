using System.Threading.Tasks;

namespace NvidiaControlPanel.Services
{
    /// <summary>
    /// Defines the contract for the simulation service.
    /// </summary>
    public interface ISimulationService
    {
        /// <summary>
        /// Retrieves the simulation configuration asynchronously.
        /// </summary>
        /// <returns>A task that represents the asynchronous operation. The task result contains the <see cref="SimulationConfig"/>.</returns>
        Task<SimulationConfig> GetConfigAsync();

        /// <summary>
        /// Retrieves the simulation configuration synchronously.
        /// </summary>
        /// <returns>The <see cref="SimulationConfig"/>.</returns>
        SimulationConfig GetConfig();

        /// <summary>
        /// Saves the simulation configuration asynchronously.
        /// </summary>
        /// <param name="config">The configuration to save.</param>
        /// <returns>A task that represents the asynchronous operation.</returns>
        Task SaveConfigAsync(SimulationConfig config);

        /// <summary>
        /// Saves the simulation configuration synchronously.
        /// </summary>
        /// <param name="config">The configuration to save.</param>
        void SaveConfig(SimulationConfig config);
    }
}
