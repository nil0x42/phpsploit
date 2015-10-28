"""PhpSploit dependencies loader

Load the listed DEPENDENCIES, falling back to the provided ones in the
current directory (./deps from PhpSploit package).
It ensures that any system missing dependency is imported anyway.

The DEPENDENCIES contains a list of tuples, instead of a dictionnary,
preventing chaotic dependency load order. First element represent the
dependency name, while the second provides it's directory path.

"""

import os
import sys
import imp
import errno

DEPENDENCIES = [('phpserialize',           'phpserialize-1.3'),
                ('colorama',               'colorama-0.2.5'),
                ('colorama_patched',       '.'),
                # ('socks',                  'SocksiPy-branch-1.02'),
                ('socks',                  'PySocks-1.4.2-61-g805d716'),
                ('sockshandler',           'PySocks-1.4.2-61-g805d716'),
                ('pyparsing',              'pyparsing-2.0.2'),
                ('shnake',                 'shnake-0.4')]

def dependency_error(module):
    sys.exit('Missing PhpSploit dependency: "%s"' % module)

for module, dirname in DEPENDENCIES:
    # try to import the dependency from system.
    try:
        __import__(module)
    # else, fallback to the provided packages.
    except ImportError:
        abspath = os.path.join(sys.path[0], __name__, dirname)
        sys.path.append(abspath)
        try:
            __import__(module)
        # if any dependency fails to load, exit with error.
        except ImportError as e:
            dependency_error(module)
        except (OSError, IOError) as e:
            if e.errno == errno.ENOENT:
                dependency_error(module)
            else:
                raise e
