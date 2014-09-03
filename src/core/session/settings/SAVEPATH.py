import tempfile

import objects
import datatypes


class SAVEPATH:
    """
    The default directory to use for saving and
    loading phpsploit sessions when a filename
    if given instead of a file path.
    """
    type = objects.settings.RandLineBuffer

    def setter(self, value):
        return datatypes.Path(value, mode="drw")

    def default_value(self):
        raw_value = tempfile.gettempdir()
        return self.setter(raw_value)
