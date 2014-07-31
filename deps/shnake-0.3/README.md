Shnake:
=======

Python3 library to make command-line tools

Introduction
------------

Shnake is a generic command interpreter with multicommand support.

The shnake library has been initially developped to correctly handle
the [phpsploit framework] shell interfaces. Therefore, it was built
in order to stand generic, and usable by any other open-source project.

- The shell part extends the pretty good `cmd` standard library, adding many
  new features, and a few new behaviors.
- The shnake lexer depends on the pyparsing library.

It was built to theorically work on all 3.x python versions.
For any bug, issue or enhancement proposal, please contact the author.

*NOTE:*
* The shnake library extends and wraps the [cmd] python standard library.
  So a little knowledge of [cmd] it required to ease shnake comprehension.


Requirements
------------

#### Mandatory dependencies:
    pyparsing

#### Optional dependencies:
    readline

_**Tested with python3.4**_

Features
--------

#### Command line interface
  * The command line interpreter has been highly enhanced, with a
    complete overwrite of the parseline() method, to provide the
    most bash-like features as possible.
  * Multi commands, separated by semicolons can now be typed.
  * Multi line command also can be written, like on bash prompt by
    ending a line with a backslash, prompting the user to continue
    writing the command in the next line (like bash's PS2).
  * Strings can now be enquoted, to be processed as a single argument.

#### Command execution
  * An argv array of arguments is now passed as do_foo() argument
    (an all other cmd related methods) instead of the [cmd] tuple.
  * The interpret() method can be used to eval a string as a list of
    shnake commands. It also can be used inside do_* commands.

#### Prompt feature
  * Included an input() wrapper (classe's raw_input() method) that
    makes use of regular expressions to automatically enclose
    enventual prompt's ANSI color codes with `\x01%s\x02`, fixing
    readline's prompt length missinterpretation on colored ones.
  * Since multiline commands are supported, a new variable:
    prompt_ps2 can be used to change PS2 prompt prefix.
  * EOFError raised during input() are the same as sending the
    `exit` command to the interpreter.

#### Exception handling
  * The new onexception() method has been made to handle exceptions.
    It eases a lot command methods (do_foo()) development, allowing
    them to simply raise exceptions on error, that will be
    automatically handled and represented by a standard error line.
  * An exception `foo` is dispatched to a method `except_foo` if
    available; the except_ method is passed a single argument, the
    exception object itself.
  * The new variable `error` defines the error line template.

#### Command return values
  * Adding support for command return values. Instead of the [cmd]
    trivial boolean behavior, any command are now able to return
    anything. The postcmd method manages integer return values, in
    a similar way than the sys.exit's behavior.
  * To leave the cmdloop() method, a SystemExit must be raised
    (with the exit() built_in function for example)

#### Misc behaviors
  * Extended the get_names() method, which now can take an instance
    as argument, limiting the returned attributes to this one.
  * Unlike [cmd] lib, emptyline()'s default behavior defaultly does
    nothing instead of repeating the last typed command (bash like).
  * Typing `EOF` to leave is not used on shnake, consider using
    `exit` and raise SystemExit instead.
  * The classe's default() method had been enhanced, writing command
    representation in case of unprintable chars, and also takes use of
    the new `nocmd` variable.
  * When left, the cmdloop() methods acts exactly in the same way
    that command return values behavior, meaning that the return
    value will be an interger anyway, 0 in case of no error.

#### Limitations & Other changes
  * Unlike [cmd] , the shnake library do not provides support for
    command line interpretation without input() built-in function.
  * Unlike [cmd], shnake is NOT compatible with python 2.x.


[phpsploit framework]: https://github.com/nil0x42/phpsploit
[cmd]: https://docs.python.org/3.4/library/cmd.html
