import objects
import datatypes


class REQ_MAX_HEADER_SIZE:
    """
    This settings defines the maximum size
    of a single header in http requests to
    the target server.

    Most http servers allow up to 4KB of data
    per http header, therefore, if the server
    administrator have configured it to a lower
    limit, execution of requests can fail and
    lead to an http error 500 or something else.
    """
    type = objects.settings.RandLineBuffer

    def setter(self, value):
        value = datatypes.ByteSize(value)
        if 250 > value:
            raise ValueError("can't be less than 250 bytes")
        return value

    def default_value(self):
        raw_value = "4 KiB"
        return self.setter(raw_value)
