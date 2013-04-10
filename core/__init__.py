"""PhpSploit framework core loader.

The core loader handles and dispatches library access methods.

Dependencies:
    Try to load PhpSploit dependencies on the running system, if
    unavailable, and since the framework installation ./lib directory
    now provides a version of each needed dependencies, they are used
    instead of needlessly raising an ImportError.

Core Modules:
    The core loader then updates the sys.path's first element, adding
    it's own name to the end, considering the new main python path as
    the ./core directory.

"""

import sys
import os.path as path

# Dependencies:
dependencies = [('phpserialize',     'phpserialize-1.3'),
                ('colorama',         'colorama-0.2.5'),
                ('colorama_patched', '.')]
for module, dirname in dependencies:
    try:
        __import__(module)
    except ImportError:
        abspath = path.join(sys.path[0], 'lib', dirname, module)
        if not path.isdir(abspath): abspath += ".py"
        import imp
        try:
            imp.load_package(module, abspath)
        except (ImportError, FileNotFoundError):
            exit('Missing PhpSploit dependency: "%s"' %module)


# Core Modules:
sys.path[0] = path.join(sys.path[0], __name__)

