#!/usr/bin/env python3
"""
Run GeForce Experience Standalone
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from geforce_experience import main

if __name__ == "__main__":
    main()
