"""User configuration manager.

Browse, initialize and load PhpSploit framework user
configuration directory and elements.

"""

import os
import errno
from . import basedir
from datatypes import Path


class UserDir:

    path = None
    choices = ["~/.config/phpsploit", "~/.phpsploit"]

    def __init__(self):
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
        # if this env var exists, add first priority choice
        if os.environ.get("XDG_CONFIG_HOME"):
            self.choices.insert(0, "$XDG_CONFIG_HOME/phpsploit")

        # normalize choices paths
        self.choices = [os.path.truepath(c) for c in self.choices]

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
        config = os.path.truepath(self.path, "config")
        if not os.path.isfile(config):
            default_config = open(basedir + "data/config/config").read()
            open(config, "w").write(default_config)

        # overwrite ./README
        readme = open(basedir + "data/config/README").read()
        open(os.path.truepath(self.path, "README"), "w").write(readme)

        # mkdirs
        dirs = ["plugins"]
        for elem in dirs:
            elem = os.path.truepath(self.path, elem)
            try:
                os.mkdir(elem)
            except IOError as e:
                if e.errno != errno.EEXIST and not os.path.isdir(elem):
                    raise e


# define user directory path
userdir = UserDir().path
