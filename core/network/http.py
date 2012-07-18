
# build an http opener taking care of proxy if exists
def build_opener(proxy):
    import urllib2
    opener = urllib2.build_opener()
    if proxy.lower() not in ['','none']:
        proxy = 'http://'+proxy
        proxyHandler = urllib2.ProxyHandler({'http':proxy,'https':proxy})
        opener.add_handler(proxyHandler)
    return(opener)

# adds all HTTP_* settings as request headers
def load_headers(settings):
    headers = dict()
    # the default user-agent string (empty here)
    headers['user-agent'] = ''

    for key,val in settings.items():
        if key.startswith('HTTP_') and key[5:]:
            key = key[5:].lower().replace('_','-')
            headers[key] = val
    return(headers)

# get real header dynamic values (to use on request sending only)
def get_headers(headers):
    from functions import getpath
    for key,val in headers.items():
        if val.lower().startswith('file://'):
            val = getpath(val[7:]).randline()
        headers[key] = val
    return(headers)
