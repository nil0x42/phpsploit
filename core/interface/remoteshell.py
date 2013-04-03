import os, sys, re
from StringIO  import StringIO

from functions      import *
from interface import core
from interface.func import *

from framework import plugins

class Start(core.CoreShell):
    shell_name = 'remote'
    # we save the old "unknow_command" as "print_unknow_command"
    print_unknow_command = core.CoreShell.unknow_command

    def __init__(self):
        """Explicitly load the CoreShell's __init__ method"""
        core.CoreShell.__init__(self)


    def preloop(self):

        # read only variables
        self.locked_env      = ['CWD']
        self.locked_settings = ['PASSKEY']
        self.CNF['CURRENT_SHELL'] = ''

        # print exploit info
        print P_inf+'Shell obtained by PHP (%s -> %s:%s)' \
            %(self.CNF['SRV']['client_addr'],
              self.CNF['SRV']['addr'],
              self.CNF['SRV']['port'])

        print P_NL+'Connected to %s server %s' \
            % (self.CNF['SRV']['os'], self.CNF['SRV']['host'])

        print 'running PHP %s with %s' \
            % (self.CNF['SRV']['phpver'], self.CNF['SRV']['soft'])

        servUpdate = False

        # if we changed target server, ask to remove ENV
        if 'ENV' in self.CNF:
            if self.CNF['SRV_HASH'] != self.CNF['SRV']['signature']:
                question = 'Server signature has changed, reset environment ?'
                if ask(question).agree():
                    del self.CNF['LNK_HASH']
                    del self.CNF['ENV']
                    print( P_inf+'Reset environment'+P_NL )
                else:
                    servUpdate = True
                    print( P_inf+'Kept environment'+P_NL )

        # set ENV default values if empty
        if not 'ENV' in self.CNF:
            self.CNF['ENV'] = dict()
            servUpdate = True

        if servUpdate:
            self.CNF['LNK_HASH'] = self.CNF['LNK']['HASH']
            self.CNF['SRV_HASH'] = self.CNF['SRV']['signature']

        # default env values if not already set
        self.default_env('CWD',          self.CNF['SRV']['home'])
        self.default_env('WEB_ROOT',     self.CNF['SRV']['webroot'])
        self.default_env('WRITE_WEBDIR', self.CNF['SRV']['write_webdir'])
        self.default_env('WRITE_TMPDIR', self.CNF['SRV']['write_tmpdir'])

        # alert for recomended ENV vars if not defined
        if not self.CNF['ENV']['WRITE_WEBDIR']:
            cmd = 'env WRITE_WEBDIR /full/path/to/writeable/web/dir'
            print(P_err+"Env warning: No writeable web directory found.")
            print(P_err+"             Use '%s' to set it." %cmd + P_NL)

        if not self.CNF['ENV']['WRITE_TMPDIR']:
            cmd = 'env WRITE_WEBDIR /full/path/to/writeable/tmp/dir'
            print(P_err+"Env warning: No writeable tmp directory found.")
            print(P_err+"             Use '%s' to set it." %cmd + P_NL)


        # Load the PhpSploit plugins
        self.plugins = plugins.Load()
        # ignore plugins whose name is identical to an existing command
        self.plugins.blacklist(self.get_commands(self))
        # then update the plugins list
        self.plugins.update()

        # load the dynamic prompt string
        self.set_prompt()


    def precmd(self, argv):
        """overwrite the unherited cmdlib's precmd() method, which
        is called just before command execution. This one handles "shell"
        command specificities, prepending the current virtual shell string
        to the use command if a virtual shell session is currently running

        """
        if not argv:
            return([])

        # virtual plugin shell handler
        if self.CNF['CURRENT_SHELL']:
            # the following conditions handle the 'shell' command capability
            # to consider commands prepended with "%" and "% " as bypassing
            # the corrent virtual plugin dedicated shell.
            if argv[0] == "%":
                argv.pop(0)
            elif argv[0].startswith("%"):
                argv[0] = argv[0][1:]
            # else, simply prepend the virtual plugin shell name as first arg
            else:
                argv.insert(0, self.CNF['CURRENT_SHELL'])

        # for stdout, except for 'lastcmd' commands
        if argv[0] != 'lastcmd':
            sys.stdout = fork_stdout(StringIO())

        return(argv)


    def postcmd(self, stop, argv):
        """overwrite the unherited cmdlib's postcmd() method, which
        is called after command execution, this one collect the last command
        output string, which has been captured by the fork_stdout() method.

        """
        try:
            self.lastcmd_data = sys.stdout.file.getvalue()
            sys.stdout.__del__()
        except:
            pass
        return(stop)


    def set_prompt(self, string=''):
        """reset the prompt string adding it's optionnal argument"""
        if string: string += ' '
        currentTarget = color(31,1)+self.CNF['LNK']['DOMAIN']+color(0)
        self.prompt = color(0,4)+'phpsploit'+color(0)
        self.prompt += '(%s) %s> ' %(currentTarget, color(1)+string+color(0))


    def default_env(self, key, value=''):
        """set the given environment value if the current is empty or unset"""
        if not key in self.CNF['ENV']:
            self.CNF['ENV'][key] = value
        elif not self.CNF['ENV'][key]:
            self.CNF['ENV'][key] = value


    def when_interrupt(self):
        """overwrite the unherited cmdlib's when_interrupt() method, which
        is called on user keyboard interrupt. This one also handles "shell"
        command specificities, disabling the current virtual shell if it
        was existing.

        """
        if not self.CNF['CURRENT_SHELL']:
            print( P_NL+self.interrupt )
        else:
            print( P_NL+P_inf+self.CNF['CURRENT_SHELL']+' shell closed.' )
            self.CNF['CURRENT_SHELL'] = ''
            self.set_prompt()


    def do_exit(self, argv):
        # NO DOCSTRING HERE
        # because it will overwrite the 'exit' help message from core.py

        #The "exit" command, which is considered as a core command
        #is in reallity rewritten on the remote shell (this one).
        #Because exiting the remote shell needs an user confirmation
        #if the current session (it it has been saved/loaded) has changed.
        #It prevents unwanted recent changes loss due to keyboard habits.

        save_ask = None
        if 'SAVEFILE' in self.CNF['SET']:
            from usr.session import load
            source = load(self.CNF['SET']['SAVEFILE'], self.CNF['PSCOREVER'])
            if source.error:
                print( source.error )
            else:
                source = source.content
                # set source SAVEFILE to check equality
                source['SET']['SAVEFILE'] = self.CNF['SET']['SAVEFILE']
                if source != self.CNF:
                    save_ask = 'The current session has changed'
        else:
            save_ask = 'The current session was not saved'
        if save_ask:
            warning  = 'if you exit now, the session changes will be lost'
            question = 'Do you really want to leave the remote shell ?'
            print( P_err+'%s, %s' %(save_ask, warning) )
            if ask(question).reject():
                return(None)
        return(True)


    #######################
    ### COMMAND: reload ###
    def do_reload(self, argv):
        """Reload the plugins list

        If you change a plugin when a phpsploit instance is already
        running, this command allows you to reload the plugins list.
        """
        """Reload the plugins list

        SYNOPSIS:
            reload

        DESCRIPTION:
            The plugins are loaded from the phpsploit installation
            directory AND from the user's 'plugins' directory, it
            exists.
            If any plugin has been changed, this command reloads them,
            so the PhpSPloit framework don't needs to be existed and
            run again before each plugin modification. Very useful
            during a plugin debugging session.
        """
        self.plugins.update()
        print( P_inf+'Plugins list reloaded' )



    ######################
    ### COMMAND: shell ###
    def complete_shell(self, text, *ignored):
        keys = self.plugins.shells()
        return([x+' ' for x in keys if x.startswith(text)])

    def do_shell(self, argv):
        """Spanws a shell plugin as prompt

        SYNOPSIS:
            shell <PLUGIN>

        DESCRIPTION:
            This command enhances the user experience while massively
            using a single command. It provides an overlay for the
            wanted command.
            - It redraws the remote shell prompt, and prepends the given
            command string to any user input command, it means that
            writing "SELECT * FROM db" from a mysql loaded shell sends
            this command "mysql SELECT * FROM db".

            It can be used with the following plugins:
              * system
              * suidroot
              * mysql
              * mssql
            And globally any other plugin which explicitly enables
            shell capability with the "api.isshell()" declaration.

        WARNING:
            To print this help message while a shell instance runs,
            the "?" command must be used.
            To exit a running shell instance, a back to the PhpSploit's
            remote shell innterface, press Ctrl-C (keyboard interrupt)
        """
        if len(argv) != 2:
            return( self.run('help shell') )

        if argv[1] in self.plugins.shells():
            quit = color(37)+'Ctrl+C'+color(0)
            help = color(37)+'?'+color(0)
            msg = '%s shell opened (use %s to leave it or %s to get help).'
            print( P_inf + msg %(argv[1], quit, help) )

            self.CNF['CURRENT_SHELL'] = argv[1]
            self.set_prompt(argv[1])
        else:
            return( self.run('help shell') )



    ########################
    ### COMMAND: lastcmd ###
    def complete_lastcmd(self, text, *ignored):
        keys = ['save','view','grep','hilight']
        return([x+' ' for x in keys if x.startswith(text)])

    def do_lastcmd(self, argv):
        """Treat the previous command's output

        Usage:   lastcmd view'
                 lastcmd save'
                 lastcmd save [file]'
                 lastcmd grep [string]'
                 lastcmd hilight [regex]'

        Example: lastcmd save /tmp/log.txt'
                 lastcmd grep mysql_connect'
        """
        """Save or view the last command's output

        SYNOPSIS:
            lastcmd view
            lastcmd save [<LOCAL FILE>]
            lastcmd grep|hilight [-i] <PATTERN>

        DESCRIPTION:
            The PhpSploit framework includes a buffer which
            contains the output of the previous command.
            The 'lastcmd' command handles this feature, and
            provides various usefull treatement options:

            * view: It basically writes the buffer's content,
                as it was before. (colors are kept)
            * save: Save the decolorized buffer's data to the
                given file path.
            * grep: Print any buffer lines which matches the
                given PATTERN. (decolorized)
            * hilight: Print the decolorized buffer, hilighting
                any section matching PATTERN

            - The PATTERN must be a python valid regular
            expression.
            - The optionnal '-i' option on the 'grep' and
            'hilight' modes makes the PATTERN case insensitive.

        EXAMPLES:
            > sysinfo; lastcmd save /tmp/remote-infos.txt
              - Save the sysinfo's output to the given file
            > phpinfo; lastcmd hilight "[Aa]pache"
              - Hilight apache or Apache strings from phpinfo
            > lastcmd grep -i foo
              - Case insensitively print any line matching foo
        """
        # collect the last command's output
        try:
            data = self.lastcmd_data
        except:
            data = ''

        # don't do anything if it is empty
        if not data:
            print( P_inf+'Last command contents is empty' )
            return(None)

        rawData = decolorize(data) # data without possible color tags

        var, val = ['','']
        if cmd['argc'] > 1: var = cmd['argv'][1]
        if cmd['argc'] > 2: val = ' '.join(cmd['argv'][2:])

        if var == 'save':
            fileName = ''
            data = decolorize(data)

            if not val:
                val = self.CNF['SET']['TMPPATH']
            val = os.path.abspath(val)
            if os.path.isdir(val):
                fileName = 'phpsploit-lastcmd.txt'

            file = getpath(val, fileName)

            writeIn = True
            if file.exists():
                question = 'File %s already exists, overwrite it ?'\
                           % quot(file.name)
                if ask(question).reject():
                    writeIn = False
                    print P_err+'The last command was not saved'
            if writeIn:
                try:
                    file.write(data)
                    print P_inf+'Last command saved in '+file.name
                except:
                    print P_err+'Writting error on '+file.name
        elif var == 'view':
            print data
        elif var == 'grep':
            lines = data.splitlines()
            print P_NL.join([x for x in lines if val.lower() in x.lower()])
        elif var == 'hilight':
            data = decolorize(data)
            tpl = '%s\\1%s' % (color(31,1), color(0))
            print( re.sub('(%s)'%val, tpl, data) )

        else:
            self.run('help lastcmd')



    ####################
    ### COMMAND: env ###
    def complete_env(self, text, *ignored):
        """use the env vars list as "env" argument completion array"""
        text = text.upper()
        completions = list()
        for key in self.CNF['ENV'].keys():
            if key.startswith(text):
                completions.append(key+' ')
        return(completions)


    def do_env(self, argv):
        """View and change environment variables.

        Usage:   env
                 env [variable]
                 env [variable] `[value|none]`

        Example: env MYSQL_BASE `information_schema`
                 env CWD
        """
        def show(*elem):
            tpl = '%s ==> '+color(1)+'%s'+color(0)
            print tpl % elem


        if len(argv) <= 2:
            # list environ matching argv[1]
            patern = argv[1] if len(argv) > 1 else ''
            title = "Environment variables"
            items = self.CNF['ENV'].items()
            elems = [(x,y) for x,y in items if x.startswith(patern)]
            if elems:
                columnize_vars(title, dict(elems)).write()
            else:
                self.run('help env')
        else:
            name = argv[1]
            value = ' '.join( argv[2:] )

            if name in self.locked_env:
                print P_err+'Locked environment variable: '+name
            elif value.lower() == 'none':
                if name in self.CNF['ENV']:
                    del self.CNF['ENV'][name]
                    print( P_inf+'Environment variable deleted: '+name )
                else:
                    self.run('help env')
            else:
                self.CNF['ENV'][name] = value
                show(name, value)



    ###############
    ### PLUGINS ###
    def unknow_command(self, argv):
        # if the unknow command is a plugin
        if argv[0] in self.plugins.commands():
            try:
                plugin = plugins.Run(argv, self.plugins, self.CNF)
                self.CNF['ENV'] = plugin.env
            except KeyboardInterrupt:
                self.when_interrupt()
        # else if it is not a plugin, call default unknow_command()
        else:
            self.print_unknow_command(argv)

