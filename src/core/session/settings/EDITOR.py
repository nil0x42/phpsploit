"""
The user's prefered text editor.

USE CASES:
  * The `set <SETTING> +` command allows user
    to dynamically edit the full buffer of a
    configuration setting. It then uses the
    EDITOR setting to open the buffer as if
    it was a file.
  * The `edit` plugin provides manual edition
    of a remote file through your local text
    editor.
"""
import os
import sys
import objects
import datatypes


type = objects.buffers.MultiLineBuffer


def setter(value):
    return datatypes.ShellCmd(value)


def default_value():
    raw_value = "vi"
    if "EDITOR" in os.environ:
        raw_value = os.environ["EDITOR"]
    elif sys.platform.startswith("win"):
        raw_value = "notepad.exe"
    return setter(raw_value)
