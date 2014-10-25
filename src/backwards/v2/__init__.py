"""Phpsploit v2 backward compatibility components

This submodule provides phpsploit framework components
which allows user to use phpsploit session files
that where created by phpsploit v2.

`v2` version refers to the core version rather than
phpsploit version tag.

This core version was active until phpsploit 2.1.4.

Session files generated from this deprecated framework
version can be recognised by their use of text-based
pickle dump, with explicit use of a PSCOREVER variable,
which is set to 2.

"""

from . import session
