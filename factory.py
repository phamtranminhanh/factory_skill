#!/usr/bin/env python3
"""
AI Software Factory Root CLI: Entry point for factory automation.
"""
import sys
from pathlib import Path

# Add core/spec-bridge to sys.path and invoke
spec_bridge_dir = Path(__file__).resolve().parent / "core" / "spec-bridge"
sys.path.insert(0, str(spec_bridge_dir))

from factory_bridge import main

if __name__ == "__main__":
    main()
