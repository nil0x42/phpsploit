"""PhpSploit framework core loader.

The core loader makes dependencies availables with the "deps" module.
Finally, it updates the main python modules path to link to itself,
making any ./core/* libraries directly available through the
python environment.

"""

# Make dependencies available:
import deps

# set basedir (phpsploit's root, aka ./), and coredir (./core) vars, then
# re bind first priority path (sys.path[0]) to coredir instead of basedir.
import sys, os.path
basedir = sys.path[0]
coredir = os.path.join(basedir, __name__)
sys.path[0] = coredir
