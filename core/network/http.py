
def build_opener(proxy):
    import urllib2
    opener = urllib2.build_opener()
    #opener.add_handler(CustomErrorHandler())
    #opener.add_handler(CustomHTTPErrorProcessor())
    #opener.add_handler(CustomHTTPDefaultErrorHandler())
    #opener.add_handler(DefaultErrorHandler())
    if proxy.lower() not in ['','none']:
        proxy = 'http://'+proxy
        proxyHandler = urllib2.ProxyHandler({'http':proxy,'https':proxy})
        opener.add_handler(proxyHandler)
    return(opener)

def load_headers(settings):
    headers = dict()
    headers['user-agent'] = '' # if no UA set, leave it empty

    for key,val in settings.items():
        if key.startswith('HTTP_') and key[5:]:
            key = key[5:].lower().replace('_','-')
            headers[key] = val
    return(headers)


def get_headers(headers):
    from functions import getpath
    for key,val in headers.items():
        if val.lower().startswith('file://'):
            val = getpath(val[7:]).randline()
        headers[key] = val
    return(headers)

### CUSTOM URLLIB2 HANDLERS:
import urllib2
class CustomHTTPErrorProcessor(urllib2.BaseHandler):
    """Process HTTP error responses."""
    handler_order = 1000  # after all other processing

    def http_error_407(self, request, response, code, msg, hdrs):
        return response

    def http_response(self, request, response):
        code, msg, hdrs = response.code, response.msg, response.info()

        # According to RFC 2616, "2xx" code indicates that the client's
        # request was successfully received, understood, and accepted.
        #if not (200 <= code < 300):
        return response

    https_response = http_response

class CustomHTTPDefaultErrorHandler(urllib2.BaseHandler):
    def http_error_default(self, req, fp, code, msg, hdrs):
        print '\nCustomHTTPDefaultErrorHandler\n'
        #raise HTTPError(req.get_full_url(), code, msg, hdrs, fp)

class DefaultErrorHandler(urllib2.HTTPDefaultErrorHandler):
    def http_error_default(self, req, fp, code, msg, headers):
        result = urllib2.HTTPError(
            req.get_full_url(), code, msg, headers, fp)
        result.status = code
        return result
