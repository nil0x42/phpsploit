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

    CNF          = None
    misc_cmds    = list()

    def __init__(self, completekey='tab', stdin=None, stdout=None):
        self.LAST_CMD_DATA = ''
        """Instantiate a line-oriented interpreter framework.

        The optional argument 'completekey' is the readline name of a
        completion key; it defaults to the Tab key. If completekey is
        not None and the readline module is available, command completion
        is done automatically. The optional arguments stdin and stdout
        specify alternate input and output file objects; if not specified,
        sys.stdin and sys.stdout are used.

        """
        if stdin is not None:  self.stdin  = stdin
        else:                  self.stdin  = sys.stdin
        if stdout is not None: self.stdout = stdout
        else:                  self.stdout = sys.stdout
        self.cmdqueue    = list()
        self.completekey = completekey

    def when_interrupt(self):
        print P_NL+self.interrupt

    def setConfig(self, config):
        """Send a CNF variable to the framework.
        """
        self.CNF = config

    def getConfig(self):
        """Returns the current CNF variable
        """
        return(self.CNF)


    def cmdloop(self, intro=None):
        """Repeatedly issue a prompt, accept input, parse an initial prefix
        off the received input, and dispatch to action methods, passing them
        the remainder of the line as argument.

        """
        if self.completekey:
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
                self.stdout.write(str(self.intro)+P_NL)
            self.preloop()
            stop = None
            while not stop:
                self.prompt = re.sub('(\x1b\[\d+?m)','\x01\\1\x02',self.prompt)
                self.prompt = self.prompt.replace('\x01\x01','\x01')
                self.prompt = self.prompt.replace('\x02\x02','\x02')
                if self.cmdqueue:
                    line = self.cmdqueue.pop(0)
                else:
                    try:
                        line = raw_input(self.prompt)
                        if not len(line): line=''
                    except EOFError:
                        print ''
                        line = 'exit'
                    except KeyboardInterrupt:
                        func = getattr(self, 'when_interrupt')
                        func()
                        line = ''
                line = self.precmd(line)
                stop = self.onecmd(line)
                stop = self.postcmd(stop, line)
            self.postloop()
        finally:
            if self.completekey:
                try:
                    import readline
                    readline.set_completer(self.old_completer)
                except ImportError:
                    pass


    def precmd(self, line):
        """Hook method executed just before the command line is
        interpreted, but after the input prompt is generated and issued.

        """

        return line

    def postcmd(self, stop, line):
        """Hook method executed just after a command dispatch is finished."""
        return stop

    def preloop(self):
        """Hook method executed once when the cmdloop() method is called."""
        pass

    def postloop(self):
        """Hook method executed once when the cmdloop() method is about to
        return.

        """
        pass

    def parseline(self, line):
        """Parse the line into a command name and a string containing
        the arguments.  Returns a tuple containing (command, args, line).
        'command' and 'args' may be None if the line couldn't be parsed.
        """
        line = line.strip()
        if not line:
            return None, None, line
        i, n = 0, len(line)
        while i < n and line[i] in self.identchars: i = i+1
        cmd, arg = line[:i], line[i:].strip()
        return cmd, arg, line

    def parseline(self, line):
        cmd = dict()
        line = line.lstrip()

        import shlex
        ok   = False
        while not ok:
            try:
                argv = shlex.split(line)
                ok = True
            except ValueError, e:
                if e.message == "No closing quotation":
                    line+= P_NL
                elif e.message == "No escaped character":
                    line = line[:-1]
                try:
                    line+= raw_input('> ')
                except KeyboardInterrupt:
                    print P_NL+P_err+'Keyboard Interrupt'
                    line = ''
                except EOFError:
                    print P_NL+P_err+'EOF Error'
                    line = ''

        cmd['line'] = line
        cmd['argv'] = argv
        cmd['argc'] = len(cmd['argv'])

        if not ' ' in line:
            cmd['name'] = line
            cmd['args'] = ''
        else:
            sep  = line.find(' ')
            cmd['name'] = line[:sep].strip()
            cmd['args'] = line[sep:].strip()

        return(cmd)


    def onecmd(self, line):
        """Interpret the argument as though it had been typed in response
        to the prompt.

        This may be overridden, but should not normally need to be;
        see the precmd() and postcmd() methods for useful execution hooks.
        The return value is a flag indicating whether interpretation of
        commands by the interpreter should stop.

        """
        cmd = self.parseline(line)
        if not cmd['line']:
            return self.emptyline()
        try:
            func = getattr(self, 'do_' + cmd['argv'][0])
        except AttributeError:
            return self.unknow_command(cmd)
        return func(cmd)

    def emptyline(self):
        """Called when an empty line is entered in response to the prompt.

        If this method is not overridden, it re loops to the prompt

        """
        return

    def unknow_command(self, cmd):
        """Called on an input line when the command prefix is not recognized.

        If this method is not overridden, it prints an error message and
        returns.

        """
        cmd = cmd['argv'][0]
        cmd_repr = repr(cmd)
        if cmd != cmd_repr[1:-1]:
            cmd = '$'+cmd_repr
        print self.nocmd % cmd

    def completedefault(self, text, line, *ignored):
        """Method called to complete an input line when no command-specific
        complete_*() method is available.

        By default, it returns an empty list.

        """
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
            if begidx>0:
                name = self.parseline(line)['name']
                if name == '':
                    compfunc = self.completedefault
                else:
                    try:
                        compfunc = getattr(self, 'complete_' + name)
                        if type(compfunc).__name__ == 'list':
                            compfunc = self.completedefault
                    except AttributeError:
                        compfunc = self.completedefault
            else:
                compfunc = self.completenames
            self.completion_matches = compfunc(text, line, begidx, endidx)
        try:
            return self.completion_matches[state]
        except IndexError:
            return None

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
        return names

    def get_commands(self, obj=None):
        commands = list()
        for method in self.get_names():
            if method.startswith('do_'):
                commands.append(method[3:])
        return commands

    def complete_help(self, *args):
        return self.completenames(*args)

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
