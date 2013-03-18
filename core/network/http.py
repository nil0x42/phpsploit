
def build_opener(proxy):
    """build the http opener for every phpsploit http request
    considering the current proxy setting, which it take as argument

    """
    import urllib2
    opener = urllib2.build_opener()
    if proxy.lower() not in ['','none']:
        proxy = 'http://'+proxy
        proxyHandler = urllib2.ProxyHandler({'http':proxy,'https':proxy})
        opener.add_handler(proxyHandler)
    return(opener)

def load_headers(settings):
    """load http headers specified as user settings, aka
    variable whose names start with HTTP_.

    it is used to get the list of user specified headers,
    with their names for http filling computing. it do not
    loads dynamic file:// objects, for this, take a look at
    the get_headers() fonction.

    """
    headers = dict()
    # the default user-agent string (empty here)
    headers['user-agent'] = ''

    for key,val in settings.items():
        if key.startswith('HTTP_') and key[5:]:
            key = key[5:].lower().replace('_','-')
            headers[key] = val
    return(headers)

def get_headers(headers):
    """this function must be used just before each unicast
    http request, because it formats eventual dynamic user
    specified header values, such as random line values
    from file:// objects.

    """
    from functions import getpath
    for key,val in headers.items():
        if val.lower().startswith('file://'):
            val = getpath(val[7:]).randline()
        headers[key] = val
    return(headers)
