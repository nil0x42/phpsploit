import objects
import datatypes


class TARGET:
    """
    The web URI to use as remote target.
    In order to run a remote exploitation session
    the given URL should be backdoored.

    NOTE: The backdoor to use can be retrieved by
          running `exploit --get-backdoor` command.
    """
    type = objects.settings.RandLineBuffer

    def setter(self, value):
        if str(value).lower() in ["", "none"]:
            return self.default_value()
        else:
            return datatypes.Url(value)

    def default_value(self):
        return None
