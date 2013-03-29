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


    def precmd(self, cmd_args):
        """overwrite the unherited cmdlib's precmd() method, which
        is called just before command execution. This one handles "shell"
        command specificities, prepending the current virtual shell string
        to the use command if a virtual shell session is currently running

        """
        # auto prepend current shell string if exists
        if self.CNF['CURRENT_SHELL']:
            cmd_args.insert(0, self.CNF['CURRENT_SHELL'])
        # fork standard output for command logging
        if cmd_args:
            if cmd_args[0] not in ['', 'lastcmd'] \
            and cmd_args != ['lastcmd', 'exit']:
                sys.stdout = fork_stdout(StringIO())

        return cmd_args


    def postcmd(self, stop, cmd_args):
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
        if string: string+=' '
        currentTarget = color(31,1)+self.CNF['LNK']['DOMAIN']+color(0)
        self.prompt = color(0,4)+'phpsploit'+color(0)
        self.prompt+= '(%s) %s> ' % (currentTarget, color(1)+string+color(0))


    def default_env(self, key, value=''):
        """set the given environment value if it's current one is
        empty or does not exist

        """
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


    def do_exit(self, cmd):
        """The "exit" command, which is considered as a core command
        is in reallity rewritten on the remote shell (this one).
        Because exiting the remote shell needs an user confirmation
        if the current session (it it has been saved/loaded) has changed.
        It prevents unwanted recent changes loss due to keyboard habits.

        """
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
    def do_reload(self, cmd):
        """Reload the plugins list

        If you change a plugin when a phpsploit instance is already
        running, this command allows you to reload the plugins list.
        """
        self.plugins.update()
        print P_inf+'Plugins list reloaded'



    ######################
    ### COMMAND: shell ###
    def help_shell(self):
        print 'This command is used to define a shell command as default'
        print 'prompt. For example, running the "shell system" command'
        print 'will pass the next typed lines to the "system" plugin'
        print 'as arguments.'
        print ''
        print 'For example, running "ls" from a "shell system" instance'
        print 'is the same than typing "system ls" from the remote shell.'
        print ''
        print 'Usage:   shell [cmdshell]'
        print ''
        print 'Available cmdshells:'
        for x in self.plugins.shells():
            print '  '+x
        print ''

    def complete_shell(self, text, *ignored):
        keys = self.plugins.shells()
        return([x+' ' for x in keys if x.startswith(text)])

    def do_shell(self, cmd):
        """Spanws a shell plugin as prompt
        """
        shell = cmd['args']
        if shell in self.plugins.shells():
            quit = color(37)+'Ctrl+C'+color(0)
            help = color(37)+'?'+color(0)
            msg = '%s shell opened (use %s to leave it or %s to get help).'
            print P_inf+msg % (shell, quit, help)
            self.CNF['CURRENT_SHELL'] = shell
            self.set_prompt(shell)
        else:
            self.help_shell()



    ########################
    ### COMMAND: lastcmd ###
    def complete_lastcmd(self, text, *ignored):
        keys = ['save','view','grep','hilight']
        return([x+' ' for x in keys if x.startswith(text)])

    def do_lastcmd(self, cmd):
        """Save or view the last command output'

        Usage:   lastcmd view'
                 lastcmd save'
                 lastcmd save [file]'
                 lastcmd grep [string]'
                 lastcmd hilight [regex]'

        Example: lastcmd save /tmp/log.txt'
                 lastcmd grep mysql_connect'
        """
        try: data = self.lastcmd_data
        except: data = ''
        if not data:
            print P_inf+'Last command contents is empty'
            return

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
            print re.sub('(%s)' % val, tpl, data)

        else:
            self.run('help lastcmd')



    ####################
    ### COMMAND: env ###
    def complete_env(self, text, *ignored):
        keys = self.CNF['ENV'].keys()
        return([x+' ' for x in keys if x.startswith(text)])

    def do_env(self, cmd):
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


        if cmd['argc'] <= 2:
            # list environ matching argv[1]
            patern = cmd['argv'][1] if cmd['argc'] > 1 else ''
            title = "Environment variables"
            items = self.CNF['ENV'].items()
            elems = [(x,y) for x,y in items if x.startswith(patern)]
            if elems:
                columnize_vars(title, dict(elems)).write()
            else:
                self.run('help env')
        else:
            var = cmd['argv'][1]
            val = ' '.join(cmd['argv'][2:])

            if var in self.locked_env:
                print P_err+'Locked environment variable: '+var
            elif val.lower() == 'none':
                if var in self.CNF['ENV']:
                    del self.CNF['ENV'][var]
                    print P_inf+'Environment variable deleted: '+var
                else:
                    self.run('help env')
            else:
                self.CNF['ENV'][var] = val
                show(var, val)



    ###############
    ### PLUGINS ###
    def unknow_command(self, cmd):
        if cmd['name'] not in self.plugins.commands():
            self.print_unknow_command(cmd)
        else:
            if cmd['args'] in ['--help','-h']:
                self.do_help(cmd['name'])
            else:
                try:
                    plugin = plugins.Run(cmd, self.plugins, self.CNF)
                    # update ENV from plugin modifications
                    self.CNF['ENV'] = plugin.env
                except KeyboardInterrupt:
                    self.when_interrupt()
