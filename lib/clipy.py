import sys, os, re, string
from functions import *


class Cmd:
    prompt       = color(4)+'phpsploit'+color(0)+' > '
    interrupt    = P_err+"Interruption: use the 'exit' command to leave the shell"
    nocmd        = P_err+'Unknown command: %s'
    nohelp       = P_err+'No help for: %s'

    identchars   = string.ascii_letters+string.digits+'_'
    ruler        = '='
    intro        = ''
    doc_leader   = ''
    doc_header   = 'Documented commands (type help <topic>):'
    misc_header  = 'Miscellaneous help topics:'
    undoc_header = 'Undocumented commands:'

    misc_cmds    = list()


    def __init__(self, completekey='tab', stdin=None, stdout=None):
        """Instantiate a line-oriented interpreter framework.

        The optional argument 'completekey' is the readline name of a
        completion key; it defaults to the Tab key. If completekey is
        not None and the readline module is available, command completion
        is done automatically. The optional arguments stdin and stdout
        specify alternate input and output file objects; if not specified,
        sys.stdin and sys.stdout are used.

        """
        if stdin is not None:
            self.stdin  = stdin
        else:
            self.stdin  = sys.stdin
        if stdout is not None:
            self.stdout = stdout
        else:
            self.stdout = sys.stdout

        self.cmdqueue = list()
        self.completekey = completekey


    def when_interrupt(self):
        """Called on user keyboard interrupt"""
        print( P_NL+self.interrupt )


    def get_prompt(self):
        """Returns the prompt string as it needs to be displayed"""
        # enclose color strings with 0x01 && 0x02 bytes, which indicates
        # to readline that these string portions must be ignored by
        # the built-in length interpreter
        formatedPrompt = re.sub('(\x1b\[\d+?m)', '\x01\\1\x02', self.prompt)
        return(formatedPrompt)


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
                self.stdout.write( str(self.intro)+P_NL )

            self.preloop()
            stop = None
            # loop while commands must be executed
            while not stop:
                # if the cmdqueue contains something, remove the first one
                # from the list and execute it.
                if self.cmdqueue:
                    argv = self.cmdqueue.pop(0) # get the command from queue
                    argv = self.precmd(argv) # optionally treat it before
                    stop = self.onecmd(argv) # execute it and get return val
                    stop = self.postcmd(stop, argv) # post command treatment

                # if the queue is empty and the last command don't required
                # to stop the current interface (return value), then pursue.
                else:
                    try:
                        prompt = self.get_prompt()
                        line = raw_input(prompt)
                    except EOFError:
                        print('')
                        line = 'exit'
                    except KeyboardInterrupt:
                        self.when_interrupt()
                        line = ''
                    # fill the cmdqueue with given user input
                    self.cmdqueue = self.parse_input(line)
            self.postloop()
        finally:
            if self.completekey:
                # reset the original readline completer
                try:
                    import readline
                    readline.set_completer(self.old_completer)
                except:
                    pass


    def run(self, cmdString):
        """Interpret the given string.
        It can be a single line, or a multiline string taken from a file
        The whole string will be parsed, then each command will be
        executed in the given order.

        'stop' indicates the return value of the given command, considering
        True as an 'exit' query. That's why a True return code interrupts
        the execution queue and stops.
        """
        cmdQueue = self.parse_input(cmdString)

        stop = False
        while cmdQueue and not stop:
            argv = cmdQueue.pop(0)
            argv = self.precmd(argv)
            stop = self.onecmd(argv)
            stop = self.postcmd(stop, argv)

        return(stop)


    def precmd(self, argv):
        """Hook method executed just before the command line is
        interpreted, but after the input prompt is generated and issued.

        """
        return(argv)


    def postcmd(self, stop, argv):
        """Hook method executed just after a command dispatch is finished."""
        return(stop)


    def preloop(self):
        """Hook method executed once when the cmdloop() method is called."""
        pass


    def postloop(self):
        """Hook method executed once when the cmdloop() method is about to
        return.
        """
        pass


    def parse_input(self, string):
        """Return a commands list from given input string, each command
        element is itself a list of single command arguments.
        For example, the string: "echo -e 'bla bla'; ls /tmp"
        Becomes: [ ["echo", "-e", "bla bla"], ["ls", "/tmp"] ]

        """
        def shlex_patch(cmd, reverse=False):
            """
            This is a patch that forces enquoted semicolons in argument list
            to be interpreted as a string instead of a command separator.
            """
            def morph_str(seq, action='encode'):
                morph = ['hex','zlib','base64']
                for m in morph+morph[::-1]:
                    seq = getattr(seq, action)(m)
                return(seq)
            patch_strings = ['\r\n', '\n', ';']
            quote_chars = ['"', "'", "`"]

            patch_strings = [(s, morph_str(s)) for s in patch_strings]
            if not reverse:
                for s,m in patch_strings:
                    for q in quote_chars:
                        cmd = cmd.replace('%s%s%s' %(q, s, q),
                                          '%s%s%s' %(q, m, q))
            else:
                for s,m in patch_strings:
                    cmd = [e.replace(m, s) for e in cmd]
            return(cmd)

        string = string.lstrip() # remove leading spaces

        # convert the input string into an arguments list (argsList)
        ok = False
        while not ok:
            try:
                from shlex import shlex
                lex = shlex( instream=shlex_patch(string), posix=True )
                lex.quotes += '`'
                lex.wordchars += '$%&()*+,-./:<=>!?@[]^_{|}~'
                lex.whitespace = ' \t'

                argsList = list(lex)
                ok = True
            except ValueError, e:
                # if the last argument quotation has not be closed, assume
                # the string as not finished, add a newline to it's end.
                if e.message == "No closing quotation":
                    string += P_NL
                # if a lines ends with an antislash, assume the pressed
                # <RETURN> key as an escaped char, then just remove it.
                elif e.message == "No escaped character":
                    string = string[:-1]
                # pursue interpretation on the next line (bash like)
                try:
                    string += raw_input('> ')
                # on Ctrl-C AND Ctrl-D, abort interpretation and flush line
                except KeyboardInterrupt:
                    print( P_NL+P_err+'Keyboard Interrupt' )
                    string = ''
                except EOFError:
                    print( P_NL+P_err+'EOF Error' )
                    string = ''

        # split the arguments list into commands list
        commandsList = list()
        start = 0
        for index in range( len(argsList) ):
            if argsList[index] in [';','\n','\r\n']:
                newCommand = argsList[start:index]
                commandsList.append( newCommand )
                start = index + 1
        commandsList.append( argsList[start:] )

        for i in range( len(commandsList) ): # reverse the patch morph
            commandsList[i] = shlex_patch(commandsList[i], reverse=True)

        return(commandsList)


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
            return( self.emptyline() )
        # call 'help <cmd>' when '<cmd> --help' is typed
        if len(argv) == 2 and argv[1] == '--help':
            return( self.run('help '+argv[0]) )

        # try to call the command's dedicated do_ method
        try:
            return( getattr(self, 'do_'+argv[0])(argv) )
        # otherwise, call unknow_command()
        except AttributeError:
            return( self.unknow_command(argv) )


    def emptyline(self):
        """Called when an empty line is entered in response to the prompt.

        If this method is not overridden, it re loops to the prompt

        """
        return


    def unknow_command(self, argv):
        """Called on an input line when the command prefix is not recognized.

        If this method is not overridden, it prints an error message and
        returns.

        """
        print( self.nocmd %raw_repr(argv[0]) )


    def completedefault(self, text, line, *ignored):
        """Method called to complete an input line when no command-specific
        complete_*() method is available.

        By default, it returns an empty list.

        """
        return([])
        try:
            cmd = line[:line.find(' ')]
            lst = getattr(self, 'complete_%s' % cmd)
            return [x for x in lst if x.startswith(text)]
        except:
            return []


    def completenames(self, text, *ignored):
        return [a+" " for a in self.get_commands() if a.startswith(text)]


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
                argv = self.parse_input(line)[-1]
                name = argv[0]
            except:
                name = None
            # if the cmd name has been entirely typed, then use it's dedicated
            # complete_*() method, or the completedefault() one otherwise.
            if begidx>0 and name in self.get_commands():
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
            return( self.completion_matches[state] )
        except IndexError:
            return( None )


    def get_names(self):
        # Inheritance says we have to look in class and
        # base classes; order is not important.
        names = []
        classes = [self.__class__]
        while classes:
            aclass = classes.pop(0)
            if aclass.__bases__:
                classes = classes + list(aclass.__bases__)
            names = names + dir(aclass)
        return( names )


    def get_commands(self, obj=None):
        commands = list()
        for method in self.get_names():
            if method.startswith('do_'):
                commands.append(method[3:])
        return commands


    def complete_help(self, *args):
        return( self.completenames(*args) )


    def do_help(self, arg):
        if arg:
            # XXX check arg syntax
            try:
                func = getattr(self, 'help_' + arg)
            except AttributeError:
                try:
                    doc=getattr(self, 'do_' + arg).__doc__
                    if doc:
                        self.stdout.write(("%s"+P_NL)%str(doc))
                        return
                    self.stdout.write(("%s"+P_NL)%str(self.nohelp % (arg,)))
                except AttributeError:
                    self.stdout.write(("%s"+P_NL)%str(self.nocmd % (arg,)))
                return
            func()
        else:
            try:
                print self.help
                return('')
            except AttributeError:
                pass
            names = self.get_names()
            cmds_doc = []
            cmds_undoc = []
            help = {}
            for name in names:
                if name[:5] == 'help_':
                    help[name[5:]]=1
            names.sort()
            # There can be duplicates if routines overridden
            prevname = ''
            for name in names:
                if name[:3] == 'do_':
                    if name == prevname:
                        continue
                    prevname = name
                    cmd=name[3:]
                    if cmd in help:
                        cmds_doc.append(cmd)
                        del help[cmd]
                    elif getattr(self, name).__doc__:
                        cmds_doc.append(cmd)
                    else:
                        cmds_undoc.append(cmd)
            self.stdout.write(("%s"+P_NL)%str(self.doc_leader))
            self.print_topics(self.doc_header,   cmds_doc,   15,80)
            self.print_topics(self.misc_header,  help.keys(),15,80)
            self.print_topics(self.undoc_header, cmds_undoc, 15,80)


    def print_topics(self, header, cmds, cmdlen, maxcol):
        if cmds:
            self.stdout.write(("%s"+P_NL)%str(header))
            if self.ruler:
                self.stdout.write(("%s"+P_NL)%str(self.ruler * len(header)))
            self.columnize(cmds, maxcol-1)
            self.stdout.write(P_NL)


    def columnize(self, list, displaywidth=80):
        """Display a list of strings as a compact set of columns.

        Each column is only as wide as necessary.
        Columns are separated by two spaces (one was not legible enough).
        """
        try: displaywidth = int(os.popen('stty size','r').read().split()[1])
        except: pass
        if not list:
            self.stdout.write("<empty>"+P_NL)
            return
        nonstrings = [i for i in range(len(list))
                        if not isinstance(list[i], str)]
        if nonstrings:
            raise TypeError, ("list[i] not a string for i in %s" %
                              ", ".join(map(str, nonstrings)))
        size = len(list)
        if size == 1:
            self.stdout.write(("%s"+P_NL)%str(list[0]))
            return
        # Try every row count from 1 upwards
        for nrows in range(1, len(list)):
            ncols = (size+nrows-1) // nrows
            colwidths = []
            totwidth = -2
            for col in range(ncols):
                colwidth = 0
                for row in range(nrows):
                    i = row + nrows*col
                    if i >= size:
                        break
                    x = list[i]
                    colwidth = max(colwidth, len(x))
                colwidths.append(colwidth)
                totwidth += colwidth + 2
                if totwidth > displaywidth:
                    break
            if totwidth <= displaywidth:
                break
        else:
            nrows = len(list)
            ncols = 1
            colwidths = [0]
        for row in range(nrows):
            texts = []
            for col in range(ncols):
                i = row + nrows*col
                if i >= size:
                    x = ""
                else:
                    x = list[i]
                texts.append(x)
            while texts and not texts[-1]:
                del texts[-1]
            for col in range(len(texts)):
                texts[col] = texts[col].ljust(colwidths[col])
            self.stdout.write(("%s"+P_NL)%str("  ".join(texts)))
