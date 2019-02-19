"""User configuration manager.

Browse, initialize and load PhpSploit framework user
configuration directory and elements.
"""
import os
import errno

import utils.path
from datatypes import Path
from . import BASEDIR


class UserDir: # pylint: disable=too-few-public-methods
    """PhpSploit Configuration Directory
    """
    path = None
    choices = ["~/.config/phpsploit", "~/.phpsploit"]

    def __init__(self):
        """Get phpsploit configuration directory,
        by checking, in this order of preference:
          - $PHPSPLOIT_CONFIG_DIR/ (only if env var exists)
          - $XDG_CONFIG_HOME/phpsploit/ (only if env var exists)
          - ~/.config/phpsploit/
          - ~/.phpsploit/

        If non of the above exist, directory creation is attempted
        with the same order of preference. Directory creation is not
        recursive, to parent directory must exist.

        If USERDIR cannot be determined, a ValueError mentioning
        last tried choice (~/.phpsploit/) is raised.
        """
        if os.environ.get("XDG_CONFIG_HOME"):
            self.choices.insert(0, "$XDG_CONFIG_HOME/phpsploit")

        if os.environ.get("PHPSPLOIT_CONFIG_DIR"):
            self.choices.insert(0, "$PHPSPLOIT_CONFIG_DIR/")

        self.choices = [utils.path.truepath(c) for c in self.choices]

        # try to find existing USERDIR
        for choice in self.choices:
            try:
                self.path = Path(choice, mode="drw")()
                break
            except ValueError:
                pass

        # try to create new valid USERDIR
        if self.path is None:
            for choice in self.choices:
                try:
                    os.mkdir(choice)
                except OSError:
                    pass
                try:
                    self.path = Path(choice, mode="drw")
                    break
                except ValueError as e:
                    if choice == self.choices[-1]:
                        raise e

        self.fill()  # finally, fill it with default content

    def fill(self):
        """Add user configuration dir's default content."""

        # create default $USERDIR/config if it doesn't exist
        config = utils.path.truepath(self.path, "config")
        if not os.path.isfile(config):
            with open(BASEDIR + "data/config/config") as file:
                default_config = file.read()
            with open(config, 'w') as file:
                file.write(default_config)

        # always override $USERDIR/README
        with open(BASEDIR + "data/config/README") as file:
            readme = file.read()
        with open(utils.path.truepath(self.path, "README"), "w") as file:
            file.write(readme)

        # create $USERDIR/plugins/ it doesn;t exist
        dirs = ["plugins"]
        for elem in dirs:
            elem = utils.path.truepath(self.path, elem)
            try:
                os.mkdir(elem)
            except OSError as e:
                if e.errno != errno.EEXIST or not os.path.isdir(elem):
                    raise e


# define user directory path
USERDIR = UserDir().path
