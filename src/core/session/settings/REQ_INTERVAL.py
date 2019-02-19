"""
Interval (in seconds) to wait between HTTP requests.

While sending large payload (like uploading a big file with
`upload` plugin), this setting can improve stealth by
preventing the remove IDS to raise alerts or block your IP
due to excess of consecutive HTTP requests.

* EXAMPLES:

# randomly sleep between 1 and 10 seconds between requests:
> set REQ_INTERVAL 1-10

# sleep exactly 3 seconds between requests:
> set REQ_INTERVAL 3
"""

import linebuf
import datatypes


linebuf_type = linebuf.RandLineBuffer


def validator(value):
    return datatypes.Interval(value)


def default_value():
    return "1-10"
