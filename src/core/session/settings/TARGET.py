"""Set target server's URL

doc
"""

import objects
import datatypes

metatype = objects.settings.RandLineBuffer


def setter(value):
    if str(value).lower() in ["", "none"]:
        return None
    else:
        return datatypes.Url(value)
