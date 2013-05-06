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
from datatypes import Path

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

    # it raises the apropriate ValueError if failed
    Path(choice, mode="edrw")


def _fill_userdir(path):
    """Add user configuration dir's default content."""
    # touch ./config
    config = os.path.truepath(path, "config")
    if not os.path.isfile(config):
        open(config, "w")

    # overwrite ./README
    readme = Path(basedir, "framework/misc/userdir.readme").read()
    open(os.path.truepath(path, "README"), "w").write(readme)

    # mkdirs
    dirs = ["plugins"]
    for elem in dirs:
        elem = os.path.truepath(path, elem)
        try:
            os.mkdir(elem)
        except FileExistsError as e:
            if not os.path.isdir(elem):
                raise e

userdir = _get_userdir()
_fill_userdir(userdir)
