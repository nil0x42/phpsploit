"""Time related functions

Author: nil0x42
"""

import re
import random
import datetime


def get_smart_date(value):
    """Return a date string usable by php strtotime()

    >>> get_smart_dable("2016-04-15 23:04:12")
    '2016-04-15 23:04:12'

    >>> # error handling with ValueError() messages
    >>> get_smart_date("2004-99-99")
    Traceback (most recent call last):
      File "<input>", line 1, in <module>
        utils.time.get_smart_date("2004-99-99")
      File "/home/user/dev/time.py", line 52, in get_smart_date
        raise ValueError("%r: %s" % (value, e))
    ValueError: '2004-99-99': format must be YYYY[-mm[-dd[ HH[:MM[:SS]]]]]

    >>> # random valid date completion when partially given
    >>> get_smart_date("2011-09")
    '2001-09-15 16:53:28'
    >>> get_smart_date("2011-09-11 13")
    '2011-09-11 13:29:42'

    NOTE:
    On phpsploit's php side, the set_smart_date()
    function can be used to generate a timestamp.

    """
    human_fmt = "YYYY[-mm[-dd[ HH[:MM[:SS]]]]]"
    python_fmt = "%Y-%m-%d %H:%M:%S"
    regex = (r"^(\d{4})(?:-(\d{2})(?:-(\d{2})(?: (\d"
             r"{2})(?::(\d{2})(?::(\d{2}))?)?)?)?)?$")
    limits = (None, (1, 12), (1, 28), (0, 23), (0, 59), (0, 59))
    try:
        items = list(re.findall(regex, value)[0])
    except IndexError:
        raise ValueError("%r: format must be %s" % (value, human_fmt))
    if int(items[0]) < 1970:
        raise ValueError("%r: min year is 1970 (EPOCH)" % value)
    for i, limit in enumerate(limits):
        if not items[i]:
            items[i] = "%02d" % random.randrange(limit[0], limit[1] + 1)
    result = "%s-%s-%s %s:%s:%s" % tuple(items)
    try:
        datetime.datetime.strptime(result, python_fmt)
    except ValueError as err:
        if python_fmt in str(err):
            err = "format must be %s" % human_fmt
        raise ValueError("%r: %s" % (value, err))
    return result
