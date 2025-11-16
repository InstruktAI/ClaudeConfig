"""
Common initialization for all hooks.
Sets up project root path and loads environment.
"""

import json  # pylint: disable=unused-import
import os  # pylint: disable=unused-import
import subprocess  # pylint: disable=unused-import
import sys

from dotenv import load_dotenv

# Project root - hardcoded from $HOME
PROJECT_ROOT = os.path.expanduser("~/.claude")

# Add to sys.path for utils imports
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Load environment
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))
