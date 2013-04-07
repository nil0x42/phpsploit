from functions import *

class fork_stdout(object):
    """this class can replace sys.stdout and writes
    simultaneously to standard output AND specified file.

    usage: fork_stdout(altFile)

    """
    def __init__(self, file):
        self.file = file
        self.stdout = sys.stdout
        sys.stdout = self

    def __del__(self):
        sys.stdout = self.stdout
        self.file.close()

    def write(self, data):
        self.file.write(data)
        self.stdout.write(data)

    def flush(self):
        self.stdout.flush()


class columnize_vars:
    """this class is used to format environment and settings output
    when printed to the interface.

    arguments: (!=required, *=optionnal)
    ! title     str,  the output's title.
    ! table     dict, the elements to output: {'key':'val'}.
    * width     int,  the output's max width; dynamic if 0.
    * color     list, a couple of colors to enhance visibility,
                      it may be left empty to disable colors.

    """
    def __init__(self, title, table, width=0, color=[color(37), color(0)]):
        self.title = title
        self.table = table
        self.width = width
        self.color = color

    def write(self):
        """print the formated output string"""
        print(self.read())

    def read(self):
        """return the formated output string"""

        # determine terminal width if not set
        if not self.width:
            self.width = termlen()

        # format self.colors value if disabled
        if not self.color:
            self.color = ['', '']

        # format the elements table
        table = list()
        maxKeyLen = 8
        for key in sorted(self.table.keys()):
            value = str(self.table[key]).strip()
            if value:
                key = str(key).strip()
                table.append((key, value))
                maxKeyLen = max(maxKeyLen, len(key))

        # generate formated output lines
        lines = str()
        for i in range( len(table) ):
            key = table[i][0]
            value = table[i][1]

            # cut overwidth values to prevent output corruption
            maxValLen = self.width - (maxKeyLen+6)
            if len(value) > maxValLen:
                cutValue = str()
                for x in range( len(value) ):
                    cutValue += value[x]
                    if not (x+1)%maxValLen:
                        cutValue += P_NL + ( ' '*(maxKeyLen+6) )
                value = cutValue

            lines += '%s    %s' %(self.color[i%2], key)
            lines += ' ' * ( 2+maxKeyLen-len(key) )
            lines += value + P_NL

        # generate the final output string
        output = [ color(0) + P_NL + self.title,
                   ( '='*len(self.title) ) + P_NL,
                   '    Variable%sValue' %(' '*(maxKeyLen-6)),
                   '    --------%s-----' %(' '*(maxKeyLen-6)),
                   lines + color(0) ]

        return P_NL.join(output)



# this function updates the self.CNF['LNK'] dict.
def update_opener(CNF):
    """update the phpsploit's opener, which is stored on the
    self.CNF['LNK'] object.

    """
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
