import tempfile

import objects
import datatypes


class TMPPATH:
    """
    Default directory to use for writing
    temporary files.
    """
    type = objects.settings.RandLineBuffer

    def setter(self, value):
        return datatypes.Path(value, mode="drw")

    def default_value(self, ):
        raw_value = tempfile.gettempdir()
        return self.setter(raw_value)
