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
import objects
import datatypes


type = objects.buffers.RandLineBuffer


def setter(value):
    if value.find("%%BASE64%%") < 0:
        raise ValueError("shall contain %%BASE64%% string")
    return datatypes.PhpCode(value)


def default_value():
    return "eval(base64_decode(%%BASE64%%))"
