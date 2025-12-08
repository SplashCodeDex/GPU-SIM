"""
Fake GPU Metrics Generator
Simulates realistic GPU utilization, temperature, and memory metrics.
"""

import random
import time
import math
import threading
from typing import Optional, Dict, List, Callable
from dataclasses import dataclass, field
from datetime import datetime

import sys
sys.path.insert(0, str(__file__).rsplit('src', 1)[0])

from src.core.gpu_profile import GPUProfile


@dataclass
class GPUMetrics:
    """Current GPU metrics snapshot."""
    timestamp: datetime = field(default_factory=datetime.now)

    # Utilization (0-100%)
    gpu_utilization: float = 0.0
    memory_utilization: float = 0.0
    encoder_utilization: float = 0.0
    decoder_utilization: float = 0.0

    # Memory (MB)
    memory_used_mb: float = 0.0
    memory_free_mb: float = 0.0
    memory_total_mb: float = 0.0

    # Clocks (MHz)
    gpu_clock_mhz: int = 0
    memory_clock_mhz: int = 0

    # Temperature (°C)
    temperature_core: float = 0.0
    temperature_memory: float = 0.0
    temperature_hotspot: float = 0.0

    # Power (W)
    power_draw_watts: float = 0.0
    power_limit_watts: float = 0.0

    # Fan (%)
    fan_speed_percent: float = 0.0

    @property
    def memory_used_percent(self) -> float:
        if self.memory_total_mb > 0:
            return (self.memory_used_mb / self.memory_total_mb) * 100
        return 0.0


class FakeMetricsGenerator:
    """
    Generates realistic-looking fake GPU metrics.
    Simulates idle, light, medium, and heavy load scenarios.
    """

    def __init__(self, profile: Optional[GPUProfile] = None):
        self._profile = profile
        self._base_metrics = GPUMetrics()
        self._current_metrics = GPUMetrics()
        self._target_load = 0.0  # 0-1 representing idle to max load
        self._running = False
        self._update_thread: Optional[threading.Thread] = None
        self._callbacks: List[Callable[[GPUMetrics], None]] = []

        # Noise parameters for realistic variation
        self._noise_amplitude = 5.0
        self._smoothing_factor = 0.3

        if profile:
            self._initialize_from_profile(profile)

    def _initialize_from_profile(self, profile: GPUProfile) -> None:
        """Initialize base values from GPU profile."""
        self._base_metrics.memory_total_mb = profile.vram_mb
        self._base_metrics.memory_free_mb = profile.vram_mb
        self._base_metrics.power_limit_watts = profile.tdp_watts
        self._base_metrics.gpu_clock_mhz = profile.base_clock_mhz
        self._base_metrics.memory_clock_mhz = profile.memory_clock_mhz

        # Reset current to idle state
        self._current_metrics = GPUMetrics(
            memory_total_mb=profile.vram_mb,
            memory_free_mb=profile.vram_mb,
            memory_used_mb=profile.vram_mb * 0.1,  # 10% baseline
            temperature_core=40.0,
            temperature_memory=38.0,
            temperature_hotspot=42.0,
            power_draw_watts=profile.tdp_watts * 0.1,
            power_limit_watts=profile.tdp_watts,
            fan_speed_percent=30.0,
            gpu_clock_mhz=profile.base_clock_mhz,
            memory_clock_mhz=profile.memory_clock_mhz,
        )

    def set_profile(self, profile: GPUProfile) -> None:
        """Update the GPU profile."""
        self._profile = profile
        self._initialize_from_profile(profile)

    def set_load(self, load_percent: float) -> None:
        """
        Set the target GPU load.

        Args:
            load_percent: 0-100 representing idle to max load.
        """
        self._target_load = max(0.0, min(100.0, load_percent)) / 100.0

    def add_callback(self, callback: Callable[[GPUMetrics], None]) -> None:
        """Add a callback for metrics updates."""
        self._callbacks.append(callback)

    def remove_callback(self, callback: Callable[[GPUMetrics], None]) -> None:
        """Remove a callback."""
        if callback in self._callbacks:
            self._callbacks.remove(callback)

    def _calculate_metrics(self) -> GPUMetrics:
        """Calculate new metrics based on target load."""
        if not self._profile:
            return GPUMetrics()

        t = time.time()
        load = self._target_load

        # Add some natural variation using sine waves
        wave1 = math.sin(t * 0.5) * 0.05
        wave2 = math.sin(t * 1.3) * 0.03
        noise = random.gauss(0, 0.02)
        variation = wave1 + wave2 + noise

        # GPU Utilization with smoothing
        target_util = load * 100 + variation * 20
        self._current_metrics.gpu_utilization = self._smooth(
            self._current_metrics.gpu_utilization,
            max(0, min(100, target_util)),
            self._smoothing_factor
        )

        # Memory Utilization (tends to stay high once loaded)
        mem_target = max(10, load * 80 + 10 + variation * 10)
        self._current_metrics.memory_utilization = self._smooth(
            self._current_metrics.memory_utilization,
            mem_target,
            self._smoothing_factor * 0.5  # Slower change
        )

        # Memory Used
        mem_used = self._profile.vram_mb * (self._current_metrics.memory_utilization / 100)
        self._current_metrics.memory_used_mb = mem_used
        self._current_metrics.memory_free_mb = self._profile.vram_mb - mem_used

        # Temperature (responds to load with delay)
        base_temp = 35
        max_temp = 85
        temp_target = base_temp + (load * (max_temp - base_temp)) + variation * 3
        self._current_metrics.temperature_core = self._smooth(
            self._current_metrics.temperature_core,
            temp_target,
            self._smoothing_factor * 0.3  # Slow thermal response
        )
        self._current_metrics.temperature_memory = self._current_metrics.temperature_core - 3
        self._current_metrics.temperature_hotspot = self._current_metrics.temperature_core + 8

        # Clocks (boost under load)
        clock_boost_factor = 1.0 + (load * 0.25)  # Up to 25% boost
        self._current_metrics.gpu_clock_mhz = int(
            self._profile.base_clock_mhz * clock_boost_factor
        )

        # Power Draw
        power_target = self._profile.tdp_watts * (0.1 + load * 0.9)
        self._current_metrics.power_draw_watts = self._smooth(
            self._current_metrics.power_draw_watts,
            power_target + variation * 10,
            self._smoothing_factor
        )

        # Fan Speed (responds to temperature)
        if self._current_metrics.temperature_core < 50:
            fan_target = 30
        elif self._current_metrics.temperature_core < 70:
            fan_target = 30 + ((self._current_metrics.temperature_core - 50) * 2)
        else:
            fan_target = 70 + ((self._current_metrics.temperature_core - 70) * 2)

        self._current_metrics.fan_speed_percent = self._smooth(
            self._current_metrics.fan_speed_percent,
            min(100, fan_target),
            self._smoothing_factor * 0.4
        )

        # Encoder/Decoder (simulate video encoding)
        if load > 0.3:
            self._current_metrics.encoder_utilization = random.uniform(0, 30) * load
            self._current_metrics.decoder_utilization = random.uniform(0, 20) * load
        else:
            self._current_metrics.encoder_utilization = 0
            self._current_metrics.decoder_utilization = 0

        self._current_metrics.timestamp = datetime.now()
        return self._current_metrics

    def _smooth(self, current: float, target: float, factor: float) -> float:
        """Apply exponential smoothing."""
        return current + (target - current) * factor

    def _update_loop(self) -> None:
        """Background update loop."""
        while self._running:
            metrics = self._calculate_metrics()

            # Notify callbacks
            for callback in self._callbacks:
                try:
                    callback(metrics)
                except Exception as e:
                    pass  # Don't let callback errors stop the loop

            time.sleep(0.1)  # 10 updates per second

    def start(self) -> None:
        """Start generating metrics in the background."""
        if self._running:
            return

        self._running = True
        self._update_thread = threading.Thread(target=self._update_loop, daemon=True)
        self._update_thread.start()

    def stop(self) -> None:
        """Stop generating metrics."""
        self._running = False
        if self._update_thread:
            self._update_thread.join(timeout=1.0)
            self._update_thread = None

    @property
    def current_metrics(self) -> GPUMetrics:
        """Get current metrics."""
        return self._current_metrics

    def get_snapshot(self) -> Dict:
        """Get metrics as a dictionary."""
        m = self._current_metrics
        return {
            "gpu_utilization": round(m.gpu_utilization, 1),
            "memory_utilization": round(m.memory_utilization, 1),
            "memory_used_mb": round(m.memory_used_mb, 0),
            "memory_total_mb": round(m.memory_total_mb, 0),
            "temperature_core": round(m.temperature_core, 1),
            "temperature_hotspot": round(m.temperature_hotspot, 1),
            "gpu_clock_mhz": m.gpu_clock_mhz,
            "power_draw_watts": round(m.power_draw_watts, 1),
            "power_limit_watts": round(m.power_limit_watts, 0),
            "fan_speed_percent": round(m.fan_speed_percent, 0),
        }


# Singleton
_metrics_generator: Optional[FakeMetricsGenerator] = None

def get_metrics_generator() -> FakeMetricsGenerator:
    """Get the singleton metrics generator."""
    global _metrics_generator
    if _metrics_generator is None:
        _metrics_generator = FakeMetricsGenerator()
    return _metrics_generator


if __name__ == "__main__":
    # Test the metrics generator
    from src.core.config_manager import get_config_manager

    config = get_config_manager()
    profiles = config.list_profiles()

    if profiles:
        profile = profiles[0]
        print(f"\nUsing profile: {profile.name}")

        generator = get_metrics_generator()
        generator.set_profile(profile)
        generator.start()

        # Simulate load changes
        print("\n📊 Simulating GPU Metrics:")
        print("-" * 50)

        try:
            for i in range(30):
                # Vary load
                if i < 5:
                    load = 10  # Idle
                elif i < 15:
                    load = 50 + i * 2  # Ramping up
                else:
                    load = 80 + random.randint(-10, 10)  # Gaming

                generator.set_load(load)
                time.sleep(0.5)

                m = generator.current_metrics
                print(f"GPU: {m.gpu_utilization:5.1f}% | "
                      f"Mem: {m.memory_used_mb:,.0f}/{m.memory_total_mb:,.0f}MB | "
                      f"Temp: {m.temperature_core:.1f}°C | "
                      f"Power: {m.power_draw_watts:.0f}W | "
                      f"Fan: {m.fan_speed_percent:.0f}%")

        except KeyboardInterrupt:
            pass
        finally:
            generator.stop()
