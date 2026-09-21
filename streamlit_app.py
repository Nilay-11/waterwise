import os
import sys

# Add directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Run WaterWise application
try:
    from app import *
except ImportError:
    from waterwise.app import *
