"""PhpSploit dependencies loader

Load the listed DEPENDENCIES, falling back to the provided ones in the
current directory (./deps from PhpSploit package).
It ensures that any system missing dependency is imported anyway.

The DEPENDENCIES contains a list of tuples, instead of a dictionnary,
preventing chaotic dependency load order. First element represent the
dependency name, while the second provides it's directory path.

"""

import os, sys, imp

DEPENDENCIES = [('phpserialize',           'phpserialize-1.3'),
                ('cmdshell',               'cmdshell-0.0.2'),
                ('colorama',               'colorama-0.2.5'),
                ('colorama_patched',       '.'),
                ('socks',                  'SocksiPy-branch-1.02'),
                ('os_path_truepath_patch', '.'),
                ('shutil_update',          '.')]

for module, dirname in DEPENDENCIES:
    # try to import the dependency from system.
    try:
        __import__(module)
    # else, fallback to the provided packages.
    except ImportError:
        abspath = os.path.join(sys.path[0], __name__, dirname, module)
        if not os.path.isdir(abspath):
            abspath += ".py"
        try:
            imp.load_package(module, abspath)
        # if any dependency fails to load, exit with error.
        except (ImportError, FileNotFoundError):
            exit('Missing PhpSploit dependency: "%s"' %module)
