import objects
import datatypes


class REQ_HEADER_PAYLOAD:
    """
    This setting allows overriding the
    encapsulator of php payloads.
    Indeed, any payload is encapsulated for
    execution of a base64 encoded string.

    General behavior of this setting shall
    keep the same logical transformation.

    NOTE: If you do not understand what you're doing,
          please do not change this setting.

    """
    type = objects.settings.RandLineBuffer

    def setter(self, value):
        if not value.find("%%BASE64%%"):
            raise ValueError("shall contain %%BASE64%% string")
        return datatypes.PhpCode(value)

    def default_value(self):
        raw_value = "eval(base64_decode(%%BASE64%%))"
        return self.setter(raw_value)
