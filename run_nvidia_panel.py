"""
NVIDIA Control Panel Launcher
Run this script to launch the fake NVIDIA Control Panel.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from nvidia_panel.nvidia_control_panel import main

if __name__ == "__main__":
    main()
