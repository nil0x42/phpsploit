"""
Interval (in seconds) to sleep between
consecutive HTTP requests.

This setting can be used to detemine how
many seconds the payload sender shall wait
between two consecutive HTTP requests.

The option only affects large payload executions
which must be sent within multiple HTTP requests
(aka, multipart payloads), by picking up a randon
interval to sleep between each of them.

If a dash separated tuple of numbers is provided,
a random value within given interval is randomly
chosen each time the setting takes effect.
The setting can also be set to a fixed value, in
which case the multipart request handler will wait
this exact number of seconds between each
consecutive request.

While sending very large payloads, such as through
the 'upload' plugin, this setting can really
improve furtivity by preventing the framework
spamming the target server with many consecutive
HTTP requests.
"""

import objects
import datatypes


type = objects.buffers.RandLineBuffer


def setter(value):
    return datatypes.Interval(value)


def default_value():
    return "1-10"
