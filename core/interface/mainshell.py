
from functions       import *
from interface       import core
from interface.func  import *

class Start(core.Shell):

    def preloop(self):
        self.do_clear('')
        softwareLogo  = getpath('misc/txt/logo.ascii').read().rstrip()
        introduction  = getpath('misc/txt/intro.msg').read().strip()
        startMessage  = getpath('misc/txt/start_messages.lst').randline()
        mainShellHelp = getpath('misc/txt/mainShell_help.msg').read().strip()
        self.help     = P_NL+mainShellHelp+P_NL

        # print intro and help
        print softwareLogo
        print ''
        print color(1)
        print introduction
        print color(0,37)
        print startMessage
        print color(0)
        print mainShellHelp
        print ''

        # inform if using session
        if 'SAVEFILE' in self.CNF['SET']:
            msg = P_inf+'Using session file %s'
            print msg % quot(self.CNF['SET']['SAVEFILE'])

        # alert if no proxy
        if self.CNF['SET']['PROXY'].lower() in ['','none']:
            err = 'No proxy gateway ! stay careful...'
            print P_err+err

        # add empty LNK if don't exist
        if not 'LNK' in self.CNF:
            self.CNF['LNK'] = dict()

        # update the LNK
        self.CNF['LNK'] = update_opener(self.CNF)


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

        if line:
            args = line.strip().split(' ')
            var  = args[0].upper()
            val  = ' '.join(args[1:])
            if var in self.CNF['SET']:
                if val:
                    backup = self.CNF['SET'][var]
                    self.CNF['SET'][var] = val
                    from usr.settings import comply
                    if comply(self.CNF['SET']):
                        show(var, self.CNF['SET'][var])
                        self.CNF['LNK'] = update_opener(self.CNF)
                    else:
                        self.CNF['SET'][var] = backup
                else:
                    show(var, self.CNF['SET'][var])
            else:
                self.help_set()
        else:
            title = "Session settings"
            items = self.CNF['SET'].items()
            elems = dict([(x.upper(),y) for x,y in items])
            columnize_vars(title, elems).write()


    ########################
    ### COMMAND: exploit ###
    def do_exploit(self, line):
        if 'URL' in self.CNF['LNK']:
            print P_inf+'Sending http payload...'
            from network import server
            link = server.Link(self.CNF)
            if link.open():
                self.CNF['SRV'] = link.srv_vars
                from interface import remoteshell
                shell = remoteshell.Start()
                shell.setConfig(self.CNF)
                shell.cmdloop()
                link.close()
        else:
            err = "Undefined target, please enable it with '%s'"
            print P_err+err % 'set TARGET <backdoored-url>'
