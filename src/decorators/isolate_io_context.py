"""A decorator for separating I/O context.
"""
import sys


def isolate_io_context(function):
    """A decorator for separating I/O context.

    This decorator isolates I/O context of target
    function or method.

    I/O Context is a mix of terminal related elements,
    such as current stdout and readline completer
    attributes.

    This decorator is useful if you run something
    that reconfigures the readline completer, or
    needs to use the default stdout file descriptor
    instead of the phpsploit's stdout wrapper.
    """
    def wrapper(*args, **kwargs):
        try:
            import readline
            handle_readline = True
        except ImportError:
            handle_readline = False

        if handle_readline:
            # backup & reset readline completer
            old_readline_completer = readline.get_completer()
            readline.set_completer((lambda x: x))
            # backup & reset readline history
            old_readline_history = []
            hist_sz = readline.get_current_history_length()
            for i in range(1, hist_sz + 1):
                line = readline.get_history_item(i)
                old_readline_history.append(line)
            readline.clear_history()
        # backup & reset stdout
        old_stdout = sys.stdout
        sys.stdout = sys.__stdout__

        try:
            retval = function(*args, **kwargs)
        finally:

            if handle_readline:
                # restore old readline completer
                readline.set_completer(old_readline_completer)
                # restore old readline history
                readline.clear_history()
                for line in old_readline_history:
                    readline.add_history(line)
            # restore old stdout
            sys.stdout = old_stdout

        return retval
    return wrapper
