"""Plugin's `plugin.py` file docstring (title line)

SYNOPSIS:
    plugin_example

DESCRIPTION:
    This plugin is a sample made to understand how
    phpsploit plugins are structured.

    If the `api` module is imported outside a real plugin
    runtime (such as with `corectl python-console`),
    then the API defaulty assumes this sample plugin as the
    current one for learning purposes.

    This text is the docstring of current plugin's
    python file (plugin.py). It means that running `help <PLUGIN>`
    will display this dicstring.

    Writting a plugin should comport a docstring formatter like
    this one, with at least a title (first line), then the
    following sections:
        SYNOPSIS
        DESCRIPTION
        AUTHOR or AUTHROS or MAINTAINERS
    
AUTHOR:
    nil0x42 <http://goo.gl/kb2wf>
"""

# standard library modules
import sys

# phpsploit framework modules
import api


print(" ".join(api.plugin.argv))
sys.exit()
