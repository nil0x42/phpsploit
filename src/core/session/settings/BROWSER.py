"""
Set attacker's default Web Browser in phpsploit's context.

* USE CASES:
The '--browser' option of `phpinfo` plugin uses this setting
to display remote server's informations locally:
> phpinfo --browser
"""
import objects
import datatypes


type = objects.linebuf.RandLineBuffer


def setter(value):
    return datatypes.WebBrowser(value)


def default_value():
    return "default"
