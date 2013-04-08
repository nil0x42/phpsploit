"""Standard Output Wrapper

This class extends and replace the standard python standard output,
aka sys.stdout, and adds some nice multiplatform relative color
support, intellligent buffer forking, and some features really
interesting for the phpsploit framework.

MEMO FOR BUILD:
>>> sys.stdout.__class__.__mro__
(<class '_io.TextIOWrapper'>, <class '_io._TextIOBase'>, <class '_io._IOBase'>, <class 'object'>)


"""



class Wrapper:
    def __init__(self):
        print('STDWOOOT!')

    def flush(self):
        pass

    def write(self):
        pass

