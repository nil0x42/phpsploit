"""User configuration manager.

Browse, initialize and load PhpSploit framework user
configuration directory and elements.

"""

import os
import errno

import utils.path
from . import BASEDIR
from datatypes import Path


class UserDir:

    path = None
    choices = ["~/.config/phpsploit", "~/.phpsploit"]

    def __init__(self):
        """Return the PhpSploit user directory.
        The following try order is used:
            0 - $PHPSPLOIT_CONFIG_DIR/ (only if env var exists)
            1 - $XDG_CONFIG_HOME/phpsploit/ (only if env var exists)
            2 - ~/.config/phpsploit/
            3 - ~/.phpsploit/

        If no one exists, an mkdir is tried for each one in the
        same order than the previous. Mkdir is not recursive,
        meaning that parent must already exist.

        If no USERDIR can be determined, a ValueError concerning
        last possible choice (~/.phpsploit/) is raised.

        """
        if os.environ.get("XDG_CONFIG_HOME"):
            self.choices.insert(0, "$XDG_CONFIG_HOME/phpsploit")

        if os.environ.get("PHPSPLOIT_CONFIG_DIR"):
            self.choices.insert(0, "$PHPSPLOIT_CONFIG_DIR/")

        # normalize choices paths
        self.choices = [utils.path.truepath(c) for c in self.choices]

        # set self.path if user directory already exist
        for choice in self.choices:
            try:
                self.path = Path(choice, mode="drw")()
                break
            except:
                pass

        # try to create it otherwise, raise err if fails
        if self.path is None:
            for choice in self.choices:
                try:
                    os.mkdir(choice)
                except:
                    pass
                try:
                    self.path = Path(choice, mode="drw")
                    break
                except Exception as e:
                    if choice == self.choices[-1]:
                        raise e

        self.fill()  # finally, fill it with default content

    def fill(self):
        """Add user configuration dir's default content."""
        # put default config if not exists
        config = utils.path.truepath(self.path, "config")
        if not os.path.isfile(config):
            with open(BASEDIR + "data/config/config") as file:
                default_config = file.read()
            with open(config, 'w') as file:
                file.write(default_config)

        # overwrite ./README
        with open(BASEDIR + "data/config/README") as file:
            readme = file.read()
        with open(utils.path.truepath(self.path, "README"), "w") as file:
            file.write(readme)

        # mkdirs
        dirs = ["plugins"]
        for elem in dirs:
            elem = utils.path.truepath(self.path, elem)
            try:
                os.mkdir(elem)
            except (OSError, IOError) as e:
                if e.errno != errno.EEXIST or not os.path.isdir(elem):
                    raise e


# define user directory path
USERDIR = UserDir().path
