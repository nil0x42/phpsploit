"""PhpSploit framework core loader.

The core loader makes dependencies availables with the "deps" module.
Finally, it updates the main python modules path to link to itself,
making any ./core/* libraries directly available through the
python environment.

vars:
=====
    basedir -> /path/to/phpsploit/
    coredir -> /path/to/phpsploit/core/
    userdir -> /home/user/.phpsploit/

"""
# deps must be imported before anything else
import deps, sys, os

# `basedir` -> 'phpsploit/' && `coredir` -> 'phpsploit/core/'
basedir = os.path.truepath(sys.path[0])
coredir = os.path.join(basedir, __name__)

# Use `coredir` as new primary python path
sys.path[0] = coredir

############### USER CONFIG DIR ################
import hashlib
from datatypes import Path

def filehash(path):
    """PhpSploit file hash signature.
    This function gives and md5sum of the file data, in a cross platform
    way, independently of the newlines.

    WARNING: The md5 hex digest returned is completely dirrefent of a
    real file md5sum.

    """
    lines = open(path, 'r').read().splitlines()
    hash = hashlib.md5( str(lines).encode('utf-8') )
    return hash.hexdigest()

# Define `userdir`, the phpsploit user config dir.
def _get_userdir():
    """Return the PhpSploit user directory.
    The following try order is used:
        0 - $XDG_CONFIG_HOME/phpsploit/ (only if env var exists)
        1 - ~/.config/phpsploit/
        2 - ~/.phpsploit/

    If no one exists, an mkdir is tried for each one in the
    same order than the previous. Mkdir is not recursive,
    meaning that parent must already exist.

    If no userdir can be determined, a ValueError concerning
    last possible choice (~/.phpsploit/) is raised.

    """
    choices = ["~/.config/phpsploit", "~/.phpsploit"]
    if os.environ.get("XDG_CONFIG_HOME"):
        choices.insert(0, "$XDG_CONFIG_HOME/phpsploit")
    choices = [os.path.truepath(c) for c in choices]

    # if a dir from `choices` exists, just return it
    for choice in choices:
        try: return Path(choice, mode="edrw")()
        except: pass

    # if no one exists, try to create one from choices
    for choice in choices:
        try:
            os.mkdir(choice)
            return Path(choice, mode="edrw")()
        except: pass

    # it raises the apropriate ValueError
    Path(choice, mode="edrw")

def _fill_userdir(path):
    """Add user configuration dir's default content.

    The default user config directory can be found at:
        ./framework/rc_template/

    """

    # this dict takes relpaths of default user config files as keys.
    # the value is a list of hashs. If one of these user config files
    # exists, it will not be overwritten, except if its current hash
    # is the same than one of the file's hash, that represent default
    # values.
    #NOTE: in order to get filehash of a file, use:
    # >>> import core
    # >>> core.filehash('/file/path')
    files = {"config"         : [],
             "plugins/README" : []}

    for filepath, defaults in files.items():
        # get path of template file
        template = Path(basedir, 'framework/rc_template', filepath)

        # add current default file content's hash to hashs list
        defaults.append(filehash(template))

        # get `path` (absolute path), and its parent dir
        path = os.path.truepath(userdir, filepath)
        dirname = os.path.dirname(path)

        # make sur file's parent directory exists
        try: os.makedirs(dirname)
        except: pass
        Path(dirname, mode="edrw")

        # if user manually changed a file, don't overwrite it:
        if os.path.exists(path) and filehash(path) not in defaults:
            continue

        # write template data to file
        open(path, 'w').write( template.read() )

userdir = _get_userdir()
_fill_userdir(userdir)
