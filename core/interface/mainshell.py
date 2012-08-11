
from functions       import *
from interface       import core
from interface.func  import *

class Start(core.CoreShell):
    shell_name = 'main'

    def __init__(self):
        core.CoreShell.__init__(self)

    def preloop(self):
        self.do_clear('')
        softwareLogo  = getpath('misc/txt/logo.ascii').read().rstrip()
        introduction  = getpath('misc/txt/intro.msg').read().strip()
        startMessage  = getpath('misc/txt/start_messages.lst').randline()

        # print intro and help
        print softwareLogo
        print ''
        print color(1)
        print introduction
        print color(0,37)
        print startMessage+color(0)
        self.run('help')

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



    ########################
    ### COMMAND: exploit ###
    def do_exploit(self, cmd):
        """Drop a shell from target server

        This command opens the remote shell.
        He sends an http request to the focused url (the one
        defined by the "TARGET" setting), and opens the
        remote shell if the dynamic payload ran.
        """
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
