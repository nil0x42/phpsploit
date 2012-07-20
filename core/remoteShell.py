import os, sys, re
from StringIO  import StringIO

from functions       import *
from framework.shell import *

from interface import cmdlib
from framework import cmdAPI


class Start(cmdlib.Cmd):

    coreHelp = dict()
    coreHelp['clear']   = 'Clear the terminal screen'
    coreHelp['debug']   = 'For tool debugging purpose'
    coreHelp['env']     = 'Change environment variables'
    coreHelp['exit']    = 'Disconnect from remote server'
    coreHelp['help']    = 'Show this help message'
    coreHelp['infect']  = 'Print the working backdoor'
    coreHelp['lastcmd'] = 'Save or view the last command output'
    coreHelp['lcd']     = 'Change local working directory'
    coreHelp['lpwd']    = 'Print local working directory'
    coreHelp['reload']  = 'Reload the plugins list'
    coreHelp['save']    = 'Save the current session in file'
    coreHelp['shell']   = 'Spanws a shell plugin as prompt'
    coreHelp['set']     = 'View and edit settings'

    def preloop(self):

        # read only variables
        self.locked_env      = ['CWD']
        self.locked_settings = ['PASSKEY']
        self.CNF['CURRENT_SHELL'] = ''

        # print exploit info
        print P_inf+'Shell obtained by PHP (%s -> %s:%s)' \
            % (self.CNF['SRV']['client_addr'], self.CNF['SRV']['addr'], self.CNF['SRV']['port'])

        print P_NL+'Connected to %s server %s' \
            % (self.CNF['SRV']['os'], self.CNF['SRV']['host'])

        print 'running PHP %s with %s' \
            % (self.CNF['SRV']['phpver'], self.CNF['SRV']['soft'])

        servUpdate = False

        # if we changed target server, ask to remove ENV
        if 'ENV' in self.CNF:
            if self.CNF['SRV_HASH'] != self.CNF['SRV']['signature']:
                response = ''
                query = 'The server signature has changed, reset environment variables ? (Y/n) : '
                print ''
                while response not in ['y','n']:
                    try: response = raw_input(P_inf+query).lower()
                    except KeyboardInterrupt: print ''
                    except: pass
                if response == 'y':
                    print P_inf+'Reset environment'+P_NL
                    del self.CNF['ENV_HASH']
                    del self.CNF['ENV']
                else:
                    print P_inf+'Keeping environment'+P_NL
                    servUpdate = True

        # set ENV default values if empty
        if not 'ENV' in self.CNF:
            self.CNF['ENV'] = dict()
            servUpdate = True

        if servUpdate:
            self.CNF['ENV_HASH'] = self.CNF['LNK']['HASH']
            self.CNF['SRV_HASH'] = self.CNF['SRV']['signature']

        # default env values if not already set
        self.default_env('CWD',          self.CNF['SRV']['home'])
        self.default_env('WEB_ROOT',     self.CNF['SRV']['webroot'])
        self.default_env('WRITE_WEBDIR', self.CNF['SRV']['write_webdir'])
        self.default_env('WRITE_TMPDIR', self.CNF['SRV']['write_tmpdir'])

        # alert for recomended ENV vars if not defined
        if not self.CNF['ENV']['WRITE_WEBDIR']:
            cmd = 'env WRITE_WEBDIR /full/path/to/writeable/web/dir'
            print P_err+"Env warning: No writeable web directory found."
            print P_err+"             Use '%s' to set it." % cmd

        if not self.CNF['ENV']['WRITE_TMPDIR']:
            cmd = 'env WRITE_WEBDIR /full/path/to/writeable/tmp/dir'
            print P_err+"Env warning: No writeable tmp directory found."
            print P_err+"             Use '%s' to set it." % cmd

        # load plugins as commands
        self.commands = cmdAPI.Loader()
        self.commands.setCore(self.coreHelp)
        self.update_commands()

        self.set_prompt()


    def precmd(self, line):
        # auto prepend current shell string if exists
        if self.CNF['CURRENT_SHELL']:
            line = self.CNF['CURRENT_SHELL']+' '+line
        # fork standard output for command logging
        l = line.strip()
        if l \
        and not l.startswith('lastcmd') \
        and l != self.CNF['CURRENT_SHELL']+' exit':
            sys.stdout = cmdlib.fork_stdout(StringIO())
        return line


    def postcmd(self, stop, line):
        try:
            self.lastcmd_data = sys.stdout.file.getvalue()
            sys.stdout.__del__()
        except:
            pass
        return stop


    def update_commands(self):
        self.commands.update()
        self.misc_cmds = self.commands.items


    def set_prompt(self, string=''):
        if string: string+=' '
        currentTarget = color(31,1)+self.CNF['LNK']['DOMAIN']+color(0)
        self.prompt = color(0,4)+'phpsploit'+color(0)
        self.prompt+= '(%s) %s> ' % (currentTarget, color(1)+string+color(0))


    def default_env(self, key, value=''):
        if not key in self.CNF['ENV']:
            self.CNF['ENV'][key] = value
        elif not self.CNF['ENV'][key]:
            self.CNF['ENV'][key] = value


    def when_interrupt(self):
        if not self.CNF['CURRENT_SHELL']:
            print P_NL+self.interrupt
        else:
            print P_NL+P_inf+self.CNF['CURRENT_SHELL']+' shell closed.'
            self.CNF['CURRENT_SHELL'] = ''
            self.set_prompt()


    ######################
    ### COMMAND: clear ###
    def do_clear(self, line):
        clear()

    ######################
    ### COMMAND: debug ###
    def do_debug(self, line):
        from pprint import pprint
        pprint(self.CNF)

    #####################
    ### COMMAND: exit ###
    def do_exit(self, line):
        return True

    #######################
    ### COMMAND: reload ###
    def do_reload(self, line):
        self.update_commands()
        print P_inf+'Plugins list reloaded'

    #####################
    ### COMMAND: save ###
    def do_save(self, line):
        import usr.session
        savedFile = usr.session.save(self.CNF, line)
        if savedFile:
            self.CNF['SET']['SAVEFILE'] = savedFile

    #######################
    ### COMMAND: infect ###
    def do_infect(self, line):
        cmd_infect(self.CNF['LNK']['BACKDOOR'])

    #####################
    ### COMMAND: lpwd ###
    def do_lpwd(self, line):
        print os.getcwd()

    ####################
    ### COMMAND: lcd ###
    def help_lcd(self):
        print 'Usage: lcd [directory]'

    def do_lcd(self, line):
        if not line:
            self.help_lcd()
        else:
            newDir = os.path.expanduser(line)
            try: os.chdir(newDir)
            except OSError, e: print P_err+str(e)[str(e).find(']')+2:]

    ######################
    ### COMMAND: shell ###
    def help_shell(self):
        print 'shell'
        print 'Spawns a shell plugin as current prompt'
        print ''
        print 'Usage:   shell [cmdshell]'
        print ''
        print 'Available cmdshells:'
        for x in self.commands.shells:
            print '  '+x
        print ''

    def complete_shell(self, text, *ignored):
        keys = self.commands.shells
        return([x+' ' for x in keys if x.startswith(text)])

    def do_shell(self, shell):
        if shell in self.commands.shells:
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
    def help_lastcmd(self):
        print 'lastcmd'
        print 'Save or view the last command output'
        print ''
        print 'Usage:   lastcmd view'
        print '         lastcmd save'
        print '         lastcmd save [file]'
        print '         lastcmd grep [string]'
        print '         lastcmd hilight [regex]'
        print ''
        print 'Example: lastcmd save /tmp/log.txt'
        print '         lastcmd grep mysql_connect'

    def complete_lastcmd(self, text, *ignored):
        keys = ['save','view','grep','hilight']
        return([x+' ' for x in keys if x.startswith(text)])

    def do_lastcmd(self, line):
        try: data = self.lastcmd_data
        except: data = ''
        if not data:
            print P_inf+'Last command contents is empty'
        else:
            args = line.strip().split(' ')
            var  = args[0].lower()
            val  = ' '.join(args[1:])
            if var == 'save':
                fileName = ''
                data = decolorize(data)

                if not val:
                    val = self.CNF['SET']['TMPPATH']
                val = os.path.abspath(val)
                if os.path.isdir(val):
                    fileName = 'phpsploit-lastcmd.txt'

                file = getpath(val, fileName)

                response = 'y'
                if file.exists():
                    query = 'File %s already exists, overwrite it ? [y/n] : '
                    response = ''
                    while response not in ['y','n']:
                        try: response = raw_input(P_inf+query % quot(file.name))
                        except: pass
                    if response == 'n':
                        print P_err+'The last command was not saved'
                if response == 'y':
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
                self.help_lastcmd()

    ####################
    ### COMMAND: env ###
    def help_env(self):
        print 'env'
        print 'View and change environment variables.'
        print ''
        print 'Usage:   env'
        print '         env [variable]'
        print '         env [variable] [value]'
        print ''
        print 'Example: env MYSQL_BASE information_schema'
        print '         env CWD'

    def complete_env(self, text, *ignored):
        keys = self.CNF['ENV'].keys()
        return([x+' ' for x in keys if x.startswith(text)])

    def do_env(self, line):
        def show(*elem):
            tpl = '%s ==> '+color(1)+'%s'+color(0)
            print tpl % elem

        if line:
            args = line.strip().split(' ')
            var  = args[0].upper()
            val  = ' '.join(args[1:])
            if var in self.CNF['ENV']:
                if val:
                    if var in self.locked_env:
                        print P_err+'Locked environment variable: '+var
                    elif val.lower() == 'none':
                        del self.CNF['ENV'][var]
                        print P_inf+'Environment variable deleted: '+var
                    else:
                        self.CNF['ENV'][var] = val
                        show(var, val)
                else:
                    show(var, self.CNF['ENV'][var])
            else:
                if not val:
                    self.help_env()
                elif val.lower() != 'none':
                    if var in self.locked_env:
                        print P_err+'Locked environment variable: '+var
                    else:
                        self.CNF['ENV'][var] = val
                        show(var, val)
        else:
            sortedEnv = dict([(x,y) for x,y in self.CNF['ENV'].items()])
            from interface.columnizer import Make as print_column
            title = "Environment variables"
            print_column(title, sortedEnv).write()


    ####################
    ### COMMAND: set ###
    def help_set(self):
        print 'set'
        print 'View and edit settings.'
        print ''
        print 'Usage:   set'
        print '         set [variable]'
        print '         set [variable] [value]'
        print ''
        print 'Example: set TEXTEDITOR /usr/bin/nano'
        print '         set PROXY None'

    def complete_set(self, text, *ignored):
        keys = self.CNF['SET'].keys()
        return([x+' ' for x in keys if x.startswith(text)])

    def do_set(self, line):

        def show(*elem):
            tpl = '%s ==> '+color(1)+'%s'+color(0)
            print tpl % elem

        def set_var(var):
            backup = self.CNF['SET'][var]
            self.CNF['SET'][var] = val
            from usr.settings import comply
            if comply(self.CNF['SET']):
                lnk_backup = self.CNF['LNK']
                self.CNF['LNK'] = update_opener(self.CNF)
                # if changed TARGET url:
                if var == 'TARGET':
                    import network.server
                    if network.server.Link(self.CNF).check():
                        self.CNF['ENV_HASH'] = self.CNF['LNK']['HASH']
                        self.set_prompt()
                    else:
                        self.CNF['LNK']      = lnk_backup
                        self.CNF['SET'][var] = backup
                else:
                    show(var, self.CNF['SET'][var])
            else:
                self.CNF['SET'][var] = backup

        if line:
            args = line.strip().split(' ')
            var  = args[0].upper()
            val  = ' '.join(args[1:])
            if var in self.CNF['SET']:
                if val:
                    if var in self.locked_settings:
                        print P_err+'Locked session setting: '+var
                    else:
                        set_var(var)
                else:
                    show(var, self.CNF['SET'][var])
            else:
                self.help_set()
        else:
            items = self.CNF['SET'].items()
            sortedSettings = dict([(x.upper(),y) for x,y in items])
            from interface.columnizer import Make as print_column
            title = "Session settings"
            print_column(title, sortedSettings).write()


    ###############
    ### PLUGINS ###
    def when_unknown(self, line):
        line = line.strip()
        if not ' ' in line:
            cmdName  = line
            cmdArgs = ''
        else:
            sep  = line.find(' ')
            cmdName = line[:sep].strip()
            cmdArgs = line[sep:].strip()

        if cmdName not in self.misc_cmds:
            print P_err+'Unknown command: '+line
        else:
            if cmdArgs in ['--help','-h']:
                self.do_help(cmdName)
            else:
                cmdData = self.commands.cmddata(cmdName)
                cmdPath = self.commands.cmdpath(cmdName)
                plugin  = (self.CNF, cmdData, cmdPath, cmdName, cmdArgs)
                try:
                    self.CNF['ENV'] = cmdAPI.Exec(*plugin)
                    del self.CNF['cmd']
                except KeyboardInterrupt:
                    self.when_interrupt()

    ############
    ### HELP ###
    def do_help(self, arg):
        if not arg:
            print self.commands.help
        else:
            try:
                func = getattr(self, 'help_'+arg)
                func()
            except AttributeError:
                if arg in self.misc_cmds:
                    cmd = self.commands.cmddata(arg)
                    print cmd['help']
                    print ''
                    print cmd['description']
                else:
                    try:
                        doc = getattr(self, 'do_'+arg).__doc__
                        if doc:
                            self.stdout.write(("%s"+P_NL)%str(doc))
                        else:
                            self.stdout.write(("%s"+P_NL)%str(self.nohelp % (arg,)))
                    except AttributeError:
                        self.stdout.write(("%s"+P_NL)%str(self.nocmd % (arg,)))
