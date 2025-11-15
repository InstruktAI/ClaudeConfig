"""
Common initialization for all hooks.
Sets up project root path and loads environment.
"""

import json  # pylint: disable=unused-import
import os  # pylint: disable=unused-import
import subprocess  # pylint: disable=unused-import
import sys
from pathlib import Path

from dotenv import load_dotenv

# Determine project root (parent of hooks/)
PROJECT_ROOT = Path(__file__).parent.parent

# Add to sys.path for utils imports
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Load environment
load_dotenv(PROJECT_ROOT / ".env")
