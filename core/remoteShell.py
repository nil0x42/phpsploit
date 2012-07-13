import os, sys, re

from functions import *
import interface.cmdlib
import framework.cmdAPI

from StringIO import StringIO


class Start(interface.cmdlib.Cmd):

    coreHelp = dict()
    coreHelp['clear']   = 'Clear the terminal screen'
    coreHelp['env']     = 'Change environment variables'
    coreHelp['exit']    = 'Disconnect from remote server'
    coreHelp['help']    = 'Show this help message'
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

        # if we changed target server, remove ENV
        if 'ENV' in self.CNF:
            if self.CNF['ENV_HASH'] != self.CNF['LNK']['HASH']:
                del self.CNF['ENV_HASH']
                del self.CNF['ENV']

        # set ENV default values if empty
        if not 'ENV' in self.CNF:
            self.CNF['ENV'] = dict()
            self.CNF['ENV_HASH'] = self.CNF['LNK']['HASH']

        # default environment variables
        self.setDefaultEnv('CWD',          self.CNF['SRV']['home'])
        self.setDefaultEnv('WEB_ROOT',     self.CNF['SRV']['webroot'])
        self.setDefaultEnv('WRITE_WEBDIR', self.CNF['SRV']['write_webdir'])
        self.setDefaultEnv('WRITE_TMPDIR', self.CNF['SRV']['write_tmpdir'])

        print 'Connected to %s server %s' % (self.CNF['SRV']['os'],     self.CNF['SRV']['host'])
        print 'running PHP %s with %s'    % (self.CNF['SRV']['phpver'], self.CNF['SRV']['soft'])

        if not self.CNF['ENV']['WRITE_WEBDIR']:
            print P_err+"Env warning: No writeable web directory found."
            print P_err+"             Use 'env WRITE_WEBDIR /full/path/to/writeable/web/dir' to set it."

        if not self.CNF['ENV']['WRITE_TMPDIR']:
            print P_err+"Env warning: No writeable tmp directory found."
            print P_err+"             Use 'env WRITE_TMPDIR /full/path/to/writeable/tmp/dir' to set it."


        self.commands = framework.cmdAPI.Loader()
        self.commands.setCore(self.coreHelp)
        self.updateCommands()

        self.setPrompt()

    def precmd(self, line):
        # auto prepend current shell string if exists
        if self.CNF['CURRENT_SHELL']:
            line = self.CNF['CURRENT_SHELL']+' '+line
        # fork standard output for command logging
        l = line.strip()
        if l and not l.startswith('lastcmd'):
            sys.stdout = fork_stdout(StringIO())
        return line

    def postcmd(self, stop, line):
        try:
            self.lastcmd_data = sys.stdout.file.getvalue()
            sys.stdout.__del__()
        except:
            pass
        return stop

    def updateCommands(self):
        self.commands.update()
        self.misc_cmds = self.commands.items

    def setPrompt(self, string=''):
        if string: string+=' '
        currentTarget = color(31,1)+self.CNF['LNK']['DOMAIN']+color(0)
        self.prompt = color(0,4)+'phpsploit'+color(0)
        self.prompt+= '(%s) %s> ' % (currentTarget, color(1)+string+color(0))

    def setDefaultEnv(self, key, value=''):
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
            self.setPrompt()

    ######################
    ### COMMAND: clear ###
    def do_clear(self, line):
        clear()

    #####################
    ### COMMAND: exit ###
    def do_exit(self, line):
        return True

    #######################
    ### COMMAND: reload ###
    def do_reload(self, line):
        self.updateCommands()
        print P_inf+'Plugins list reloaded'

    #####################
    ### COMMAND: save ###
    def do_save(self, line):
        import usr.session
        savedFile = usr.session.save(self.CNF, line)
        if savedFile:
            self.CNF['SET']['SAVEFILE'] = savedFile

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

    def complete_shell(self, text, line, begidx, endidx):
        completions = self.commands.shells
        if text:
            completions = [x+' ' for x in completions if x.startswith(text)]
        return(completions)

    def do_shell(self, line):
        if line in self.commands.shells:
            xcmds = (color(37)+'Ctrl+C'+color(0), color(37)+'?'+color(0))
            print P_inf+line+' shell opened (use %s to leave it or %s to get help).' % xcmds
            self.CNF['CURRENT_SHELL'] = line
            self.setPrompt(line)
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
        print ''
        print 'Example: lastcmd save /tmp/log.txt'
        print '         lastcmd grep mysql_connect'

    def complete_lastcmd(self, text, *ignored):
        keys = ['save','view','grep']
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
                defName = 'phpsploit-lastcmd.txt'
                if not val: val= getpath(self.CNF['SET']['TMPPATH'], defName).name
                val = os.path.abspath(val)
                if os.path.isdir(val): val = getpath(val, defName).name
                data = re.sub('(\x1b\[\d+?m)','',data)
                response = 'y'
                if os.path.exists(val):
                    query = 'File %s already exists, overwrite it ? [y/n] : ' % quot(val)
                    response = ''
                    while response not in ['y','n']:
                        try: response = raw_input(P_inf+query)
                        except: pass
                    if response == 'n':
                        print P_err+'The last command was not saved'
                if response == 'y':
                    try:
                        open(val,'w').write(data)
                        print P_inf+'Last command saved in '+val
                    except:
                        print P_err+'Writting error on '+val
            elif var == 'view':
                print data
            elif var == 'grep':
                print P_NL.join([x for x in data.splitlines() if val.lower() in x.lower()])
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

    def complete_env(self, text, line, begidx, endidx):
        completions = self.CNF['ENV'].keys()
        if text:
            completions = [x+' ' for x in completions if x.startswith(text)]
        return(completions)

    def do_env(self, line):
        def showStatus(*nameAndVal):
            template = '%s ==> '+color(1)+'%s'+color(0)
            print template % nameAndVal

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
                        showStatus(var, val)
                else:
                    showStatus(var, self.CNF['ENV'][var])
            else:
                if not val:
                    self.help_env()
                elif val.lower() != 'none':
                    if var in self.locked_env:
                        print P_err+'Locked environment variable: '+var
                    else:
                        self.CNF['ENV'][var] = val
                        showStatus(var, val)
        else:
            sortedEnv = dict([(x,y) for x,y in self.CNF['ENV'].items()])
            import interface.columnizer
            title = "Environment variables"
            interface.columnizer.Make(title,sortedEnv).write()


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

    def complete_set(self, text, line, begidx, endidx):
        completions = self.CNF['SET'].keys()
        if text:
            completions = [x for x in completions if x.startswith(text)]
        return(completions)

    def do_set(self, line):
        def showStatus(*nameAndVal):
            template = '%s ==> '+color(1)+'%s'+color(0)
            print template % nameAndVal

        if line:
            args = line.strip().split(' ')
            var  = args[0].upper()
            val  = ' '.join(args[1:])
            if var in self.CNF['SET']:
                if val:
                    if var in self.locked_settings:
                        print P_err+'Locked session setting: '+var
                    else:
                        oldValue = self.CNF['SET'][var]
                        self.CNF['SET'][var] = val
                        import usr.settings
                        if usr.settings.comply(self.CNF['SET']):
                            showStatus(var, self.CNF['SET'][var])
                            #self.updateOpener()
                        else:
                            self.CNF['SET'][var] = oldValue
                else:
                    showStatus(var, self.CNF['SET'][var])
            else:
                self.help_set()
        else:
            items = self.CNF['SET'].items()
            sortedSettings = dict([(x.upper(),y) for x,y in items])
            import interface.columnizer
            title = "Session settings"
            interface.columnizer.Make(title,sortedSettings).write()


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
                self.CNF['ENV'] = framework.cmdAPI.Exec(self.CNF,cmdData,cmdPath,cmdName,cmdArgs)

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
