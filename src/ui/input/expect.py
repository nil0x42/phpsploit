"""Easily ask for user choice from terminal"""
__all__ = ["Expect"]

import os
import sys
import signal

from decorators.isolate_readline_context import isolate_readline_context

from ..color import colorize
from ..output import isatty


class Expect: # pylint: disable=too-few-public-methods
    """Expect some user input, and provide response related to the
    instance configuration variables.

    It instantiates an input query, according the configured
    variables (detailed below). To send it to input, use __call__()
    (python magic method).

    NOTE: Since the default prompted question can be defined in
    object instanciation, it also can be overwritten by giving a string
    as argument on the __call__() method:
    >>> choices = ['children', 'teenager']
    >>> ask = Expect(expect=choices, case_sensitive=True)
    >>> ask.question = 'How young is your son ?'
    >>> ask() # asks default question (set just above)
    >>> ask('How young are you ?') # overwrite default question

    VARIABLES:

    * expect (default: None)
        The expected response handler, may be bool, list, str or None.
        - If set to None (default), then any response, even if empty
        will be accepted, and returned as it is.
        - If set to bool, aka True or False, a [Yes|No] response is
        expected. A boolean will also be returned, True, is response is
        empty or the same as expected, False otherwise.
        For example, `Expect(False)('are you ready')` will return True
        is response is No (starts with 'n') or empty, and returns False
        if the response is Yes (starts with 'y') because False, aka No
        was expected.
        - If set to a string, the question will be re-asked while the
        expected string has not been typed.
        - If set to a list, then any one of these elements is expected,
        and the matching one is returned. NOTE: In this mode, the first
        list's element is automatically considered as the default one.

    * question (default: '')
        The asked question string, prefixing input expectation. If not
        empty, the input question's magic tag (BoldPink '[?]')
        automatically prefixes it.

    * timeout (default: 0)
        Integer allowing to define a time limit to the expected input.
        It time is reached, then the default choice will be returned,
        bypassing user input expectation. If zero, timeout is disabled.

    * default (default: None)
        If not None, this attribute overwrites the default expected
        input if the user left it empty, or if the current input is not
        a tty.

    * case_sensitive (default: False)
        Since defaulty set to False, the default behavior is to be
        case insensitive about user response. For example, for bool
        expectations whose response must be 'y' or 'n', uppercase
        strings will also be accepted. Set it to True to claim strict
        responses.

    * append_choices (default: True)
        Indicates whether an expected choices representation must be
        appended to the question string or no. Defaultly, it is set
        to True, so expecting a reponse like this:
        `Expect(expect=False, append_choices=True)('Exit now ?')`
        will prompt the user for: "[?] Exit now ? [y/N] ", with default
        choice (here False, aka "N") ansi bolded.

    * skip_interrupt (default: True)
        If set to True (default), it prevents KeyboardInterrupt and
        EOFError interruptions, and re ask the question instead of
        raising them.


    NOTE: If stdin is detached from user tty (aka, if the command is
    being interpreted without interface), then the default response is
    automatically triggered, as if it was typed by the user.

    """

    def __init__(self, expect=None, question='', timeout=0,
                 default=None, case_sensitive=False,
                 append_choices=True, skip_interrupt=True):

        self.expect = expect
        self.question = str(question)
        self.timeout = int(timeout)
        self.default = default
        self.case_sensitive = bool(case_sensitive)
        self.append_choices = bool(append_choices)
        self.skip_interrupt = bool(skip_interrupt)

    @isolate_readline_context
    def __call__(self, question=None):

        # use custom question, or fallback to the default one.
        if question is not None:
            question = str(question)
        else:
            question = self.question
        # auto prepend question magic tag: "[?]" (if non empty):
        if question:
            question = "[?] " + question.lstrip()

        expect = self.expect
        default = ''

        # handle yes/no choice (expect=bool)
        if isinstance(expect, bool):
            expect = ['y', 'n']
            default = expect[not self.expect]

        # handle multi choice (expect=list)
        elif isinstance(expect, list) and expect:
            default = expect[0]

        # handle single choice (expect=str):
        elif isinstance(expect, str):
            expect = [expect]

        # self.default overwites default if not None
        if self.default is not None:
            default = str(self.default)

        # clean out
        default = str(default).strip()
        if expect is not None:
            expect = [str(e).strip() for e in expect]

        # case sensitivity
        if not self.case_sensitive:
            default = default.lower()
            if expect is not None:
                expect = [e.lower() for e in expect]

        # handle append_choices query suffix:
        append_choices = self.append_choices
        if append_choices and expect is not None:
            suffix = colorize('%BoldCyan', ' [')
            sep = '/' if '/' not in str(expect) else ' || '
            sep = colorize('%BoldCyan', sep)
            items = [e.strip() for e in expect if e.strip()]
            for index, item in enumerate(items):
                if default == item:
                    if not self.case_sensitive:
                        item = item.upper()
                    items[index] = colorize('%BoldWhite') + item
                else:
                    if not self.case_sensitive:
                        item = item.lower()
                    items[index] = colorize('%BasicWhite') + item
            suffix += sep.join(items) + colorize('%BoldCyan', '] ')
            if items:
                question = question.rstrip() + suffix

        # force timeout = 1 if not interactive:
        if isatty():
            timeout = self.timeout
        else:
            timeout = 1

        # ask loop
        while True:
            response = None
            # start timeout that calls illegal lambda (raising TypeError)
            signal.signal(signal.SIGALRM, lambda: 0)
            signal.alarm(timeout)
            sys.stdout.write(question)
            sys.stdout.flush()
            try:
                response = sys.stdin.readline()
                if os.linesep in response:
                    response = response.replace(os.linesep, "")
                else:
                    raise EOFError
            except BaseException as e:
                print()
                # if skip interrupt, just reloop, otherwise, raise
                if type(e) in (EOFError, KeyboardInterrupt):
                    if self.skip_interrupt:
                        continue
                    else:
                        raise e
                # if timeout reached, use `default` as response
                elif type(e) == TypeError:
                    response = default
                # normally raise unplanned exceptions
                else:
                    raise e
            signal.alarm(0)

            # if None is expected, any response is accepted
            if expect is None:
                if default and not response:
                    return str(default)
                return response

            # use default response if not given
            if not response:
                response = default

            if not self.case_sensitive:
                response = response.lower()

            if response in expect:
                # if boolean was expected, return True in the case
                # response is the same as expected. False otherwise
                if isinstance(self.expect, bool):
                    resp = response == "y"
                    return resp == self.expect
                # just return response otherwise
                return response
