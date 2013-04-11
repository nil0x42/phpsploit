"""PhpSploit framework core loader.

The core loader makes dependencies availables with the "deps" module.
Finally, it updates the main python modules path to link to itself,
making any ./core/* libraries directly available through the
python environment.

"""

# Make dependencies available:
import deps

# Make ./core/* libs available:
import sys, os.path
sys.path[0] = os.path.join(sys.path[0], __name__)
