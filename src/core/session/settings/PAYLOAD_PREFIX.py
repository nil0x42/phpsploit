"""
This setting aims to provide a way to deeply
customize special cases while executing payloads.

The PAYLOAD_PREFIX's contains a PHP code that will
be executed just before at the start of all sent
php payloads.

NOTE: If you do not understand what you're doing,
      please do not change this setting.
"""
import core
import objects
import datatypes


type = objects.buffers.MultiLineBuffer


def setter(value):
    return datatypes.PhpCode(value)


def default_value():
    file_relpath = "data/tunnel/payload_prefix.php"
    file = datatypes.Path(core.basedir, file_relpath)
    return file.read()
