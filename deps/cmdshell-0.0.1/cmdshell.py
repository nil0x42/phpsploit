"""A generic command interpreter with multicommand support.

The cmdshell library extends the (very good) python 'cmd' library, and
provides many new features to it:

1 - Keyboard interrupt handling with the 'interrupt' string and
    when_interrupt() hook method.
2 - Advanced bash simulation, with multi command support with semicolon
    and newline separation.
3 - Newline escape with backslash, like in bash.
4 - Fixed ansi colored prompt length missinterpretation with readline.
5 - New run() method, that interprets a string like if it was typed in
    the user input.
6 - The parseline() method supports multiline and returns a list of
    commands, each command is an argv list.
7 - Unlike 'cmd', cmdshell don't provide support of interpretation
    withou rawinput.
8 - Empty line re-loops instead of re running the last typed command
9 - Added get_names() object limitation by argument.


"""




import cmd, shlex, re, bz2

class Cmd(cmd.Cmd):
    interrupt    = "Interruption: run 'exit' to quit"
    unknow       = "*** Unknown command: %s"
    prompt_ps2   = "> "

    def __init__(self, completekey='tab', stdin=None, stdout=None):
        cmd.Cmd.__init__(self, completekey=completekey, \
                         stdin=stdin, stdout=stdout)


    def when_interrupt(self):
        """hook method executed on user keyboard interrupt"""
        self.stdout.write('\n'+self.interrupt+'\n')


    def raw_input(self, prompt):
        """Returns a readline aware prompt string for input, that
        encloses ansi codes to make its length ignored readline

        """
        try: import readline
        except: return input(prompt)

        pattern = "\x01?(\x1b\[((?:\d|;)*)([a-zA-Z]))\x02?"
        return input( re.sub(pattern, "\x01\\1\x02", prompt) )


    def cmdloop(self, intro=None):
        """Repeatedly issue a prompt, accept input, parse an initial prefix
        off the received input, and dispatch to action methods, passing them
        the remainder of the line as argument.

        """
        if self.completekey:
            # optionally import the readline module
            try:
                import readline
                self.old_completer = readline.get_completer()
                readline.set_completer(self.complete)
                readline.parse_and_bind(self.completekey+": complete")
            except ImportError:
                pass
        try:
            if intro:
                self.intro = intro
            if self.intro:
                self.stdout.write( str(self.intro)+"\n" )

            self.preloop() # pre command hook method

            stop = None
            while not stop:
                # run queued command is any
                if self.cmdqueue:
                    argv = self.cmdqueue.pop(0)
                    argv = self.precmd(argv)
                    stop = self.onecmd(argv)
                    stop = self.postcmd(stop, argv)

                # if no queue, get new user input
                else:
                    try:
                        line = self.raw_input(self.prompt)
                    except EOFError:
                        self.stdout.write('\n')
                        line = 'exit'
                    except KeyboardInterrupt:
                        self.when_interrupt()
                        line = ''
                    # fill cmd queue with input commands
                    self.cmdqueue = self.parseline(line)

            self.postloop() # post command hook method

        finally:
            if self.completekey:
                # reset original readline completer
                try:
                    import readline
                    readline.set_completer(self.old_completer)
                except ImportError:
                    pass


    def run(self, cmdString):
        """Interpret the given command(s) string.
        Supports multiline and semicolon separation for multi commands.
        The whole string is parsed, then executed one by one.

        """
        cmdQueue = self.parseline(cmdString)
        stop = False
        while cmdQueue and not stop:
            argv = cmdQueue.pop(0)
            argv = self.precmd(argv)
            stop = self.onecmd(argv)
            stop = self.postcmd(stop, argv)
        return stop


    def parseline(self, string):
        """Parse the input into a list of 'argv' elements for each command.
        Example:
        >>> parseline("echo -e 'foo bar'; ls /tmp")
        [["echo", "-e", "bla bla"], ["ls", "/tmp"]]

        """
        def shlex_patch(cmd, reverse=False):
            """Force enquoted separators to not be interpreted as such"""
            patch_strings = ['\r\n', '\n', ';']
            quote_chars = ['"', "'", "`"]
            patch_strings = [(s, str(hash(s))) for s in patch_strings]
            if not reverse:
                for s,m in patch_strings:
                    for q in quote_chars:
                        cmd = cmd.replace('%s%s%s' %(q, s, q),
                                          '%s%s%s' %(q, m, q))
            else:
                for s,m in patch_strings:
                    cmd = [e.replace(m, s) for e in cmd]
            return cmd

        string = string.lstrip()

        # get a list of arguments from custom shlex configuration
        # Example: ['ls','-a',';','help']
        ok = False
        while not ok:
            try:
                lex = shlex.shlex( instream=shlex_patch(string), posix=True )
                lex.quotes += '`'
                lex.wordchars += '$%&()*+,-./:<=>!?@[]^_{|}~'
                lex.whitespace = ' \t'
                arguments = list(lex)
                ok = True
            except ValueError as e:
                # if the last argument quotation has not be closed, assume
                # the string is unfinished, and add a newline to it's end.
                if e.message == "No closing quotation":
                    string += '\n'
                # if a lines ends with an antislash, assume the pressed
                # <RETURN> key as an escaped char, then just remove it.
                elif e.message == "No escaped character":
                    string = string[:-1]
                # pursue interpretation on the next line (bash like)
                try:
                    string += self.raw_input(self.prompt_ps2)
                except (EOFError, KeyboardInterrupt):
                    string = ''

        # separate arguments by commands [['ls','-a'],['help']]
        commands = []
        begidx = 0
        for idx, arg in enumerate(arguments):
            if arg in [';','\n','\r\n']:
                new = arguments[begidx:idx]
                commands.append(new)
                begidx = idx + 1
        commands.append( arguments[begidx:] ) # add last command args

        for idx, cmd in enumerate(commands): # reverse the patch morph
            commands[idx] = shlex_patch(cmd, reverse=True)

        return commands


    def onecmd(self, argv):
        """Interpret the argument as though it had been typed in response
        to the prompt.

        This may be overridden, but should not normally need to be;
        see the precmd() and postcmd() methods for useful execution hooks.
        The return value is a flag indicating whether interpretation of
        commands by the interpreter should stop.

        """
        # call emptyline() if no arguments
        if not argv:
            return self.emptyline()
        # call 'help <cmd>' when '<cmd> --help' is typed
        if len(argv) == 2 and argv[1] == '--help':
            return self.run('help '+argv[0])
        # try to call the command's dedicated do_ method
        try:
            return getattr(self, 'do_'+argv[0])(argv)
        # otherwise, fallback to default()
        except AttributeError:
            return self.default(argv)


    def emptyline(self):
        """Called when an empty line is entered in response to the prompt.

        By default, it does nothing (unless the 'cmd' lib behavior)

        """
        return


    def default(self, argv):
        """Called on an input line when the command prefix is not recognized.

        If this method is not overridden, it prints an error message and
        returns.

        """
        cmdRepr = "${!r}".format(argv[0])
        cmd = argv[0] if argv[0] == cmdRepr[2:-1] else cmdRepr
        self.stdout.write((self.unknow+'\n') %cmd)


    def complete(self, text, state):
        """Return the next possible completion for 'text'.

        If a command has not been entered, then complete against command list.
        Otherwise try to call complete_<command> to get list of completions.
        """
        if state == 0:
            import readline
            origline = readline.get_line_buffer()
            line = origline.lstrip()
            stripped = len(origline) - len(line)
            begidx = readline.get_begidx() - stripped
            endidx = readline.get_endidx() - stripped

            # get the current command's name (argv[0])
            try:
                name = self.parseline(line)[-1][0]
            except:
                name = None
            # if the cmd name has been entirely typed, then use it's dedicated
            # complete_*() method, or fallback to completedefault().
            if begidx>0:
                try:
                    compfunc = getattr(self, 'complete_'+name)
                except AttributeError:
                    compfunc = self.completedefault
            # if the cmd name is being typed, completion must suggest the
            # available commands list, aka completenames()
            else:
                compfunc = self.completenames
            self.completion_matches = compfunc(text, line, begidx, endidx)
        try:
            #print()
            #print()
            #import pprint
            #pprint.pprint(self.completion_matches[state])
            #print()
            #print()
            #return [e+' ' for e in self.completion_matches[state]]
            return self.completion_matches[state]+' '
        except IndexError:
            return


    def get_names(self, obj=None):
        """Pull in 'obj' base class attributes (defaults to self)"""
        if obj is None:
            return dir(self.__class__)
        return dir(obj.__class__)


    def do_help(self, argv):
        'List available commands with "help" or detailed help with "help cmd".'
        print(self.__class__.mro())
        argv.append('')
        super(Cmd, self).do_help(argv[1])


    def do_exit(self, argv):
        'Leave the shell interface'
        self.stdout.write("*** Command shell left with 'exit'\n")
        return True
