"""
User's prefered web browser.

This setting can be overridden if automatic
detection of system's web browser fails,
or if you want to use another one for
commands that needs to know what web browser
to use.

USE CASES:
  * The `phpinfo` plugin's '--browser' option
    uses this setting to display server's
    phpinfo() output.
"""
import objects
import datatypes


type = objects.buffers.RandLineBuffer


def setter(value):
    return datatypes.WebBrowser(value)


def default_value():
    return "default"
