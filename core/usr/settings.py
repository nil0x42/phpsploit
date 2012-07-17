import os, re, string
from functions import *

userFile = getpath('~/.phpsploitrc')
softFile = getpath('phpsploit.conf')
template = getpath('misc/conf/settings.tpl')

def load():
    configFile = get_file()
    userSettings    = get_settings(configFile)
    defaultSettings = get_settings(defaultConf)
    settings = merge(userSettings, defaultSettings)
    return(settings)

def merge(main, default):
    for key,value in default.items():
        if not key in main:
            main[key] = value
    return(main)

def get_file():
    if userFile.isfile():
        return(userFile)
    elif softFile.isfile():
        return(softFile)
    else:
        userFile.write(defaultConf)
        return(userFile)

def gen_config():
    config = template.read()

    # GET EXTERNAL APPLICATIONS
    externalApps = re.findall('%%WHICH/(.+?)%%',config)
    cmd = ['which','where'][os.name == 'nt']
    for apps in externalApps:
        appName = ''; c=0
        choices = apps.split(',')
        while not appName:
            if c == len(choices):
                appName = ' '
            else:
                req = cmd+' '+choices[c].lower()
                res = os.popen(req).read().splitlines()
                res = (res+[''])[0].strip()
                if os.path.isabs(res):
                    appName = res
            c+=1
        config = config.replace('%%WHICH/'+apps+'%%',appName.strip())

    # GET LOCAL TEMPORARY DIR
    import tempfile
    tempDir = tempfile.gettempdir()
    config  = config.replace('%%TEMPDIR%%',tempDir)
    return(config)

defaultConf = gen_config()

def get_settings(configFile):
    try:    lines = configFile.readlines()
    except: lines = configFile.splitlines()
    settings = dict()
    for line in lines:
        isAValidLine = line.split('#')[0].strip()
        if isAValidLine and '=' in line:
            sep   = line.find('=')
            name  = line[:sep].strip()
            value = line[sep+1:].strip()
            settings[name] = value
    return(settings)

# check if all settings are conform
def comply(settings):
    global status
    status = True

    def setError(name,msg):
        global status
        errorMsg = P_err+'Settings error: '+quot(name)+': '
        print errorMsg+msg
        status = False

    for name,value in settings.items():

        if name == 'PASSKEY':
            reserved_headers = ['host','accept-encoding','connection',
                                'user-agent','content-type','content-length']
            if not value:
                setError(name,'Is empty')

            # condition disabled, SRVHASH is no more supported
            # because it troubles changing target during a running session
            # (if the passkey is SRVHASH, and target on same server use another
            # hostname, the domain hashkey will change, making impossible to know
            # what real backdoor we have to use with the "infect" command.
            ### if value != '%%SRVHASH%%':
            if True:
                value = value.lower()
                if not re.match('^[a-z0-9_]+$',value):
                    #err = 'Only alphanumeric chars and underscore'
                    #err+= ' OR %%SRVHASH%% are accepted'
                    err = 'Accepted chars: a-zA-Z_'
                    setError(name,err)
                if re.match('^zz[a-z]{2}$',value) \
                or value.replace('_','-') in reserved_headers:
                    err = 'The value %s is a reserved header name'
                    setError(name, err % quot(value))

        elif name == 'BACKDOOR':
            if not '%%PASSKEY%%' in value:
                setError(name,'Have to contain %%PASSKEY%%')

        elif name == 'TMPPATH':
            if not os.path.isdir(value):
                setError(name,'Not a directory')
            elif not os.path.isabs(value):
                setError(name,'Not an absolute path')
            elif not getpath(value).access('w'):
                setError(name,'Directory write permission denied')

        elif name == 'SAVEPATH':
            if not os.path.isdir(value):
                setError(name,'Not a directory')
            elif not os.path.isabs(value):
                setError(name,'Not an absolute path')
            elif not getpath(value).access('w'):
                setError(name,'Directory write permission denied')

        elif name == 'SAVEFILE':
            if not os.path.isabs(value):
                setError(name, 'Not an absolute path')

        elif name == 'PROXY':
            err=0
            value = value.lower()
            if value not in ['','none']:
                sep = value.find(':')
                if not sep: err=1
                host = value[:sep]
                port = value[sep+1:]
                try: x=int(port)
                except: err=1
                if err:
                    setError(name,"Accepted values are host:port OR None")

        elif name == 'TARGET':
            value = value.lower()
            if value not in ['','none']:
                domainParser = '^https?://(.+?)(?:$|/)'
                try:    matchedDomain = re.findall(domainParser,value)[0]
                except: matchedDomain = ''
                if not matchedDomain or len(value)<14:
                    setError(name,"Needs to be a valid URL")

        elif name == 'REQ_INTERVAL':
            if getinterval(value) is None:
                err = "Needs to be a number or a range (ex: '1.5 - 10')"
                setError(name, err)

        elif name == 'REQ_DEFAULT_METHOD':
            if value.upper() not in ['GET','POST']:
                setError(name, "Accepted values are GET or POST")

        elif name == 'REQ_HEADER_PAYLOAD':
            if not '%%BASE64%%' in value:
                setError(name,'Have to contain %%BASE64%%')

        elif name == 'REQ_MAX_HEADERS':
            try:
                value = int(value)
            except:
                setError(name,"Needs to be numeric")
            if value < 10:
                setError(name,"Can't be smaller than 10")
            elif value > 680:
                setError(name,"Can't be higher than 680")

        elif name == 'REQ_MAX_HEADER_SIZE':
            value = octets(value)
            if value < 250:
                setError(name, "Needs to be a number of at least 250 bytes")

        elif name == 'REQ_MAX_POST_SIZE':
            value = octets(value)
            if value < 250:
                setError(name, "Needs to be a number of at least 250 bytes")

        elif name == 'REQ_ZLIB_TRY_LIMIT':
            value = octets(value)
            if value < 1:
                setError(name, "Needs to be a number of at least 1 byte")

        elif name.startswith('HTTP_') and name[5:] \
        and  value.lower().startswith('file://'):
            path = getpath(value[7:])
            if not path.isfile() or not path.access('r'):
                setError(name, value+" is not a readable file")
            elif not path.randline():
                setError(name, value+" is an empty file")

    return(status)
