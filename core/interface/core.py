import os

from functions import *
from interface.func import *

from interface import cmdlib

class CoreShell(cmdlib.Cmd):
    shell_name = 'core'

    def __init__(self):
        cmdlib.Cmd.__init__(self)
        self.locked_settings = []
        self.locked_env      = []


    def get_commands(self, obj=None):
        """Used to get a list of do_* commands in specified object
        no argument lists ALL commands, including core, shell and
        plugin commands
        """
        commands = list()
        if obj is None:
            try: commands = self.plugins.commands()
            except: pass
            obj = self
        for method in dir(obj):
            if method.startswith('do_'):
                commands.append(method[3:])
        commands = list(set(commands))
        commands.sort()
        return(commands)


    def run(self, line):
        """this function runs the line specified as argument
        """
        return self.onecmd(line)


    #####################
    ### COMMAND: exit ###
    def do_exit(self, cmd):
        """Leave the current shell

        If you are in a remote exploitation shell,
        this command disconnects you, then back to
        the phpsploit main shell.

        When you are in the main shell, this command
        just leaves the framework.
        """
        return True


    ######################
    ### COMMAND: clear ###
    def do_clear(self, cmd):
        """
        Clear the terminal screen

        This command clears the terminal screen,
        it's only usefull for shell visibility.

        """
        cmd = ['clear','cls'][os.name == 'nt']
        os.system(cmd)

    #####################
    ### COMMAND: rtfm ###
    def do_rtfm(self, line):
        """Read the fine manual

        This command show you the phpsploit's user manual.
        On unix systems, he tries to show it with the
        "man" system command. Else, just writes the manual
        to standard output.
        """
        def _printit():
            print getpath('readme/README').read()
        if os.name == 'nt':
            _printit()
        else:
            cmd = 'man %s' % getpath('readme/MANUAL').name
            if os.system(cmd):
                _printit()


    #######################
    ### COMMAND: infect ###
    def do_infect(self, cmd):
        """Print the working backdoor

        Show the backdoor that you need to inject into the
        target server, in the webpage defined by "TARGET"
        setting. One it is injected, you can run the "exploit"
        command to spawn a remote shell.
        """
        backdoor = self.CNF['LNK']['BACKDOOR']
        length   = len(backdoor)
        print ''
        print 'To infect the target'
        print 'Insert this backdoor on TARGET url:'
        print ''
        print ''+'='*length
        print ''+color(34)+backdoor+color(0)
        print ''+'='*length
        print ''


    #####################
    ### COMMAND: save ###
    def do_save(self, cmd):
        """Save the current session in file

        This feature is very usefull to keep working phpsploit
        sessions in a file.
        The default directory used to save
        them is defined by the "SAVEPATH" setting, and the
        default filename is "phpsploit.session".
        If the "SAVEFILE" setting is defined, the command
        will use it as filepath if no argument if defined.

        Usage:   save
                 save [directory]
                 save [filepath]
        Example: save ./
                 save /tmp/my-sploit-session.txt
        """
        from usr.session import save
        try:    arg = cmd['argv'][1]
        except: arg = ''
        savedFile = save(self.CNF, arg)
        if savedFile:
            self.CNF['SET']['SAVEFILE'] = savedFile


    #####################
    ### COMMAND: lpwd ###
    def do_lpwd(self, cmd):
        """Print local working directory

        This command print the local working directory
        from your own local system.
        You can use the "lcd" command to move to
        another directory.
        """
        print os.getcwd()


    ####################
    ### COMMAND: lcd ###
    def do_lcd(self, cmd):
        """Change local working directory

        The "lcd" command is an exuivalent to the unix
        command "cd", that will change the current directory
        in your local system (the "cd" command is a built-in
        plugin that do the same for the remote target system).

        Usage:   lcd [directory]
        Example: lcd ~
                 lcd /tmp/ram
        """
        if cmd['argc'] != 2:
            self.run('help lcd')
        else:
            newDir = os.path.expanduser(cmd['argv'][1])
            try: os.chdir(newDir)
            except OSError, e: print P_err+str(e)[str(e).find(']')+2:]


    #######################
    #### COMMAND: debug ###
    def do_debug(self, line):
        """For tool debugging purpose

        This command is only used to dump the current session
        variables for phpsploit debugging purpose.
        Only helpful for developpers.
        """
        from pprint import pprint
        pprint(self.CNF)


    ####################
    ### COMMAND: set ###
    def complete_set(self, text, *ignored):
        keys = self.CNF['SET'].keys()
        return([x+' ' for x in keys if x.startswith(text)])

    def do_set(self, cmd):
        """View and edit settings

        Usage:   set
                 set [variable]
                 set [variable] [value]

        Example: set TEXTEDITOR /usr/bin/nano
                 set PROXY None
        """
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
                # if we are in the remoteShell
                if self.shell_name == 'remote':
                    # if changed TARGET url:
                    if var == 'TARGET':
                        import network.server
                        if network.server.Link(self.CNF).check():
                            self.CNF['LNK_HASH'] = self.CNF['LNK']['HASH']
                            self.set_prompt()
                        else:
                            self.CNF['LNK']      = lnk_backup
                            self.CNF['SET'][var] = backup
                    else:
                        show(var, self.CNF['SET'][var])
                else:
                    show(var, self.CNF['SET'][var])
            else:
                self.CNF['SET'][var] = backup

        var, val = ['','']
        if cmd['argc'] > 1: var = cmd['argv'][1]
        if cmd['argc'] > 2: val = ' '.join(cmd['argv'][2:])
        if var in self.CNF['SET']:
            if val:
                if var in self.locked_settings:
                    print P_err+'Locked session setting: '+var
                else:
                    set_var(var)
            else:
                show(var, self.CNF['SET'][var])
        elif var:
            self.run('help set')
        else:
            title = "Session settings"
            items = self.CNF['SET'].items()
            elems = dict([(x.upper(),y) for x,y in items])
            columnize_vars(title, elems).write()



    #####################
    ### COMMAND: help ###
    def do_help(self, cmd):
        """Show commands help

        Usage:   help
                 help [command]
        Example: help infect
        """
        if cmd['argc'] > 2:
            self.run('help help')

        sys_commands = self.get_commands(self)

        def get_doc(arg):
            try: doc = self.plugins.get(arg, 'help')
            except: doc = None
            if arg in sys_commands:
                doc = getattr(self, 'do_'+arg).__doc__
            if doc is None:
                try: doc = getattr(CoreShell, 'do_'+arg).__doc__
                except: doc = None
            if doc is None:
                return('')
            return(doc.strip().splitlines())

        def get_description(doc):
            try: return doc[0].strip()
            except: return color(33)+'No description'+color(0)

        def doc_help(doc):
            if len(doc)<2:
                return
            doc = doc[1:]
            for n in range(0, len(doc)):
                if doc[n].strip():
                    doc = doc[n:]
                    break
            trash = len(doc[0])-len(doc[0].lstrip())
            doc = [x[trash:].rstrip() for x in doc]
            print P_NL.join(doc)

        # command help
        if cmd['argc'] == 2:
            arg = cmd['argv'][1]
            doc = get_doc(arg)
            if not doc:
                print self.nocmd % arg
                return
            print P_inf+arg
            print P_inf+get_description(doc)+P_NL
            try:
                getattr(self, 'help_'+arg)()
            except:
                doc_help(doc)
            return

        # generic help
        maxlen = max(13, len(max(sys_commands, key=len)))
        core_commands  = self.get_commands(CoreShell)
        shell_commands = [x for x in sys_commands if x not in core_commands]


        help = [('Core Commands',core_commands),
                ('Shell Commands',shell_commands)]
        #try:
        if self.shell_name == 'remote':
            # try to load plugin groups
            for category in self.plugins.categories():
                name   = 'Pspapi: %s Commands' \
                         % category.replace('_',' ').capitalize()
                items  = self.plugins.list_category(category)
                maxlen = max(maxlen, len(max(items, key=len)))
                help+=[(name, items)]
        #except: pass

        for group, commands in help:
            # loop to print help categories
            print P_NL+group+P_NL+('='*len(group))+P_NL
            print '    Command'+(' '*(maxlen-5))+'Description'
            print '    -------'+(' '*(maxlen-5))+'-----------'
            commands.sort()
            for name in commands:
                space = ' '*(maxlen-len(name)+2)
                description = get_description(get_doc(name))
                print '    '+name+space+description
            print ''
