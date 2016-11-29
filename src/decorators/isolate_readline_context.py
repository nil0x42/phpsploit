"""A decorator for separating readline context.

This decorator isolates readline context of target
function or method.

Use when phpsploit's readline context should be
reset temporarly is the context of triggering
function or method.

Unlike `isolate_io_context`, this decorator keeps
original stdout wrapper.
"""


def isolate_readline_context(function):
    def wrapper(*args, **kwargs):
        try:
            import readline
            handle_readline = True
        except:
            handle_readline = False

        # backup phpsploit I/O context
        if handle_readline:
            old_readline_completer = readline.get_completer()
            readline.set_completer((lambda x: x))
        # execute function with fresh context
        try:
            retval = function(*args, **kwargs)
        # restore phpsploit I/O context
        finally:
            if handle_readline:
                readline.set_completer(old_readline_completer)
        # return function result
        return retval
    return wrapper
