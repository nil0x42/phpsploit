import os

from functions import *
from interface.func import *

from interface import cmdlib

class Shell(cmdlib.Cmd):


    #####################
    ### COMMAND: exit ###
    def do_exit(self, line):
        return True


    ######################
    ### COMMAND: clear ###
    def do_clear(self, line):
        cmd = ['clear','cls'][os.name == 'nt']
        os.system(cmd)


    #####################
    ### COMMAND: rtfm ###
    def do_rtfm(self, line):
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
    def do_infect(self, line):
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
    def do_save(self, line):
        from usr.session import save
        savedFile = save(self.CNF, line)
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


    #######################
    #### COMMAND: debug ###
    def do_debug(self, line):
        from pprint import pprint
        pprint(self.CNF)
