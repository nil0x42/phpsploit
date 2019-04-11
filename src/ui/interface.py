"""PhpSploit shell interface

Handles general behavior of Phpsploit interactive command-line interface.
"""
# pylint: disable=too-many-lines
# pylint: disable=too-many-public-methods
__all__ = ["Shell"]

import os
import traceback
import shnake

import core
from core import session, tunnel, plugins, encoding
import datatypes
from datatypes import Path
import ui.output
from ui.color import colorize
import ui.input
import utils.path

READLINE_COMPLETER_DELIMS = ' \t\n`~!#$%^&*()=+[{]}\\|;:\'",<>?'


class Shell(shnake.Shell):
    """PhpSploit shell interface"""

    prompt = colorize('%Lined', 'phpsploit', '%Reset', ' > ')

    _nocmd = "[-] Unknown Command: %s"
    nohelp = "[-] No help for: %s"
    error = "[!] %s"

    bind_command = None

    def __init__(self):
        self.nocmd = None
        self.last_exception = None
        super().__init__()
        try:
            import readline
            readline.set_history_length(session.Hist.MAX_SIZE)
            readline.set_completer_delims(READLINE_COMPLETER_DELIMS)
        except ImportError:
            pass

    def init(self):
        """phpsploit interface init"""
        # load phpsploit plugins list
        plugins.blacklist = self.get_names(self, "do_")
        plugins.reload(verbose=False)

    # pylint: disable=arguments-differ
    def precmd(self, argv):
        """Handle pre command hooks such as session aliases"""
        # Make 'nocmd' error message explicit if tunnel is connected
        self.nocmd = self._nocmd
        if tunnel:
            self.nocmd += " (use `run` plugin to run remote command)"
        # Reset backlog before each command except backlog
        if self.bind_command:
            if len(argv) == 1 and argv[0] == "exit":
                # self.bind_command = None
                pass
            else:
                argv.insert(0, self.bind_command)
        if argv and argv[0] != "backlog":
            self.stdout.backlog = ""
        # Alias Handler
        try:
            cmds = self.parseline(session.Alias[argv[0]])
        except (KeyError, IndexError):
            return argv
        self.interpret(cmds[:-1], precmd=(lambda x: x))
        return cmds[-1] + argv[1:]

    def onecmd(self, argv):
        if "id" in session.Compat and session.Compat["id"] == "v1":
            print("[-] Warning: You are using a v1-compatible session file")
            print("[-]          please upgrade $TARGET with new $BACKDOOR")
            print("[-]          and run `session upgrade` when done.")
            print("")
        print("[#] %s: Running..." % self.debug_cmdrepr(argv))
        return super().onecmd(argv)

    def postcmd(self, retval, argv):
        """Post command hook

        Redraw shell prompt
        """
        int_retval = self.return_errcode(retval)
        print("[#] %s: Returned %d" % (self.debug_cmdrepr(argv), int_retval))
        # redraw shell prompt after each command
        prompt_elems = ["%Lined", "phpsploit"]
        if tunnel:
            # if remote shell, add target hostname to prompt
            prompt_elems += ["%Reset", "(", "%BoldRed",
                             tunnel.hostname, "%Reset", ")"]
        if self.bind_command:
            # If a command is binded to the prompt
            prompt_elems += ["%ResetBoldWhite", " #", self.bind_command]
        prompt_elems += ["%Reset", " > "]
        self.prompt = colorize(*prompt_elems)

        return retval

    def completenames(self, text, line, *_):
        """Add aliases and plugins for completion"""
        argv = line.split()
        if (len(argv) == 2 and line and line[-1] == " ") or len(argv) > 2:
            return []
        result = super().completenames(text, line, *_)
        result += list(session.Alias)
        if tunnel:
            result += list(plugins)
        return [x for x in list(set(result)) if x.startswith(text)]

    def onexception(self, exception):
        """Add traceback handler to onexception"""
        exc = traceback.format_exception(type(exception),
                                         exception,
                                         exception.__traceback__)
        # a small patch for traceback from plugins, remove trash lines
        for idx, line in enumerate(exc):
            if ('File "<frozen importlib._bootstrap>"' in line
                    and '_call_with_frames_removed' in line):
                exc = exc[(idx + 1):]
                header = "Traceback (most recent call last):"
                exc.insert(0, header + os.linesep)
                break
        self.last_exception = "".join(exc).splitlines()
        for line in self.last_exception:
            print(colorize("[#] ", "%Red", line))
        return super().onexception(exception)

    def default(self, argv):
        """Fallback to plugin command (if any)"""
        if argv[0] in plugins.keys():
            if tunnel:
                return plugins.run(argv)
            self.nocmd = "[-] Must connect to run `%s` plugin (`help exploit`)"
        return super().default(argv)

    #################
    # COMMAND: exit #
    @staticmethod
    def complete_exit(text, line, *_):
        """autocompletion for `exit` command"""
        argv = line.split()
        if (len(argv) == 2 and line[-1] == " ") or len(argv) > 2:
            return []
        keys = ["--force"]
        return [x for x in keys if x.startswith(text)]

    def do_exit(self, argv):
        """Quit current shell interface

        SYNOPSIS:
            exit [--force]

        OPTIONS:
            --force
                When called to leave the framework, this
                option forces exit, avoiding warning message
                if current session has not been saved to a file,
                or has changed since last save.

        DESCRIPTION:
            If current phpsploit session is connected to $TARGET,
            this command disconnects the user from remote session.
            Otherwise, if the interface is not connected, this
            command leaves the phpsploit framework.
        """
        if len(argv) == 2 and argv[1] == "--force":
            force_exit = True
        elif len(argv) == 1:
            force_exit = False
        else:
            self.interpret("help exit")
            return False

        if self.bind_command:
            self.bind_command = None
        elif tunnel:
            tunnel.close()
        else:
            if not force_exit:
                try:
                    session_changed = session.diff(None)
                except OSError:
                    session_changed = bool(tunnel.has_been_active())
                if session_changed:
                    msg = "Do you really want to exit without saving session ?"
                    if ui.input.Expect(False)(msg):
                        return False
            exit()
        return True # make pylint happy

    ####################
    # COMMAND: corectl #
    @staticmethod
    def complete_corectl(text, line, *_):
        """autocompletion for `corectl` command"""
        argv = line.split()
        if (len(argv) == 2 and line[-1] == " ") or len(argv) > 2:
            return []
        keys = ["stack-traceback", "reload-plugins",
                "python-console", "display-http-requests"]
        return [x for x in keys if x.startswith(text)]

    def do_corectl(self, argv):
        """Advanced core debugging utils

        SYNOPSIS:
            corectl <TOOL>

        CORECTL TOOLS:
        --------------

        stack-traceback
            Print the full track trace of last python exception.

            Error messages (lines that starts with a `[!]` red tag)
            are generated by a thrown exception.
            The `stack-traceback` tool displays the full python
            stack trace of the last thrown exception.
            This command is useful for debugging purposes.

            NOTE: stack traceback is NOT saved in session files

        reload-plugins
            Reload all phpsploit plugins.

            By default, the list of phpsploit plugins is loaded
            once only, when the framework starts.
            Therefore, plugin developpers may want to reload
            the plugins in order to be able to test their
            plugin modifications without having to restart the
            framework each time.

        python-console
            Run a python interpreter.

            The python console interpreter is a good gateway for deep
            debugging, or to get help about a phpsploit module, class,
            object, such as the plugin developpers API.

            For help with the API, run the following commands inside
            the python console:
            >>> import api
            >>> help(api)

        display-http-requests
            Display HTTP(s) request(s) for debugging

            Shows all HTTP(s) request(s) that were sent in the last
            remote command execution.

            NOTE: http requests are NOT saved in session files
            WARNING: don't works with HTTPS requests (see issue #29 on github)
        """
        argv.append('')

        if argv[1] == "stack-traceback":
            if not self.last_exception:
                print("[-] Exception stack is empty")
                return False
            for line in self.last_exception:
                print(colorize("%Red", line))
            return True

        if argv[1] == "reload-plugins":
            return plugins.reload(verbose=True)

        if argv[1] == "python-console":
            from ui import console
            console = console.Console()
            console.banner = "Phpsploit corectl: python console interpreter"
            return console()

        if argv[1] == "display-http-requests":
            requests = tunnel.get_raw_requests()
            if not requests:
                print("[-] From now, phpsploit didn't "
                      "sent any HTTP(s) request")
                return False
            print("[*] Listing last payload's HTTP(s) requests:\n")
            for num, request in enumerate(requests, 1):
                print("#" * 78)
                print("### REQUEST %d" % num)
                print("#" * 78)
                print(encoding.decode(request))
            return True

        self.interpret("help corectl")
        return False

    ####################
    # COMMAND: history #
    def do_history(self, argv):
        """Command line history

        SYNOPSIS:
            history [<COUNT>]

        DESCRIPTION:
            Returns a formatted string giving the event number and
            contents for each of the events in the history list
            except for current event.

            If [COUNT] is specified, only the [COUNT] most recent
            events are displayed.

            > history
              - Display the full history of events.
            > history 10
              - Display last 10 commands of the history.
        """
        import readline

        argv.append('9999999999')

        try:
            count = int(argv[1])
        except ValueError:
            return self.interpret("help history")

        last = readline.get_current_history_length()
        while last > session.Hist.MAX_SIZE:
            readline.remove_history_item(0)
            last -= 1
        first = last - count
        if first < 1:
            first = 1
        for i in range(first, last):
            cmd = readline.get_history_item(i)
            print("{:4d}  {:s}".format(i, cmd))

    ####################
    # COMMAND: exploit #
    @staticmethod
    def complete_exploit(text, line, *_):
        """autocompletion for `exploit` command"""
        argv = line.split()
        if (len(argv) == 2 and line[-1] == " ") or len(argv) > 2:
            return []
        keys = ["--get-backdoor"]
        return [x for x in keys if x.startswith(text)]

    def do_exploit(self, argv):
        """Spawn a shell from target server

        SYNOPSIS:
            exploit [--get-backdoor]

        DESCRIPTION:
            Connect to remote target URL (`help set TARGET`).

            If backdoor (`exploit --get-backdoor`) is correctly
            injected in target URL, phpsploit spawns a remote shell.

        OPTIONS:
            --get-backdoor
                Display current backdoor code, as it should be
                injected on target URL.
        """
        obj = str(session.Conf.BACKDOOR(call=False))
        obj = obj.replace("%%PASSKEY%%", session.Conf.PASSKEY().upper())

        if len(argv) > 1:
            if argv[1] == "--get-backdoor":
                print(obj)
                return True
            self.interpret("help exploit")
            return False

        print("[*] Current backdoor is: " + obj + "\n")

        if tunnel:
            m = ("[*] Use `set TARGET <VALUE>` to use another url as target."
                 "\n[*] To exploit a new server, disconnect from «{}» first.")
            print(m.format(session.Env.HOST))
            return False

        if session.Conf.TARGET() is None:
            m = ("To run a remote tunnel, the backdoor shown above must be\n"
                 "manually injected in a remote server executable web page.\n"
                 "Then, use `set TARGET <BACKDOORED_URL>` and run `exploit`.")
            print(colorize("%BoldCyan", m))
            return False

        return tunnel.open()  # it raises exception if fails

    #################
    # COMMAND: rtfm #
    @staticmethod
    # pylint: disable=unused-argument
    def do_rtfm(argv):
        """Read the fine manual

        SYNOPSIS:
            rtfm

        DESCRIPTION:
            Display phpsploit user manual. If available, the `man`
            command is used for display. Otherwise, a text version
            of the man page is displayed in phpsploit interface.
        """
        man = Path(core.BASEDIR, 'man/phpsploit.1')
        cmd = 'man phpsploit 2>/dev/null || man %r 2>/dev/null' % man
        if os.system(cmd) != 0:
            txt_man = Path(core.BASEDIR, 'man/phpsploit.txt')
            print(txt_man.read())

    ####################
    # COMMAND: session #
    @staticmethod
    def complete_session(text, line, *_):
        """autocompletion for `session` command"""
        argv = line.split()
        if (len(argv) == 2 and line[-1] != " ") or len(argv) == 1:
            keys = ['save', 'diff', 'upgrade']
            if tunnel:
                keys.append("load")
            return [x for x in keys if x.startswith(text)]
        if (len(argv) == 2 and line[-1] == " ") \
                or (len(argv) == 3 and line[-1] != " "):
            if argv[1] in ["save", "load", "diff"]:
                if os.path.isfile(session.File):
                    return [session.File]
        return []

    @staticmethod
    def do_session(argv):
        """phpsploit session handler

        SYNOPSIS:
            session [load|diff] [<FILE>]
            session save [-f] [<FILE>]
            session upgrade

        DESCRIPTION:
            The `session` core command handles phpsploit sessions.
            Sessions can be considered as phpsploit instances. They
            handle current configuration settings, environment vars,
            command aliases, and remote tunnel attributes (if any).
            They can be saved to a file for further use.

        USAGE:
            * session [<FILE>]
                Show a nice colored representation of FILE session
                content. If called without argument, current session
                if displayed.
            * session diff [<FILE>]
                Show a textual representation of the differences
                between FILE and current session. If FILE is not set,
                the diff between session's original and current states
                if shown.
            * session save [-f] [<FILE>]
                Save current session state in FILE.
                If FILE is not set, the session is saved to it's original
                path location. It still not bound to a file, default location
                is '$SAVEPATH/phpsploit.session'.
                NOTE: The '-f' option, if used, saves the session without
                      asking user confirmation if file already exists.
            * session load [<FILE>]
                Try to load session from FILE.
                It unset, try to load session from './phpsploit.session'
            * session upgrade
                If current session file is in v1-compatible mode,
                the request handler is limited to POST method and does
                not supports multi request and stealth modules.
                This command shall be used to upgrade current session
                AFTER you upgraded the remote $TARGET with new-style
                phpsploit backdoor (which can be obtained with
                `exploit --get-backdoor` command).

        EXAMPLES:
            > session load /tmp/phpsploit.session
              - Load /tmp/phpsploit.session.
            > session save
              - Save current state to session file.

        WARNING:
            `session load` should NEVER be used while still connected
            to a remote TARGET. If you want to load another session,
            first run `exit` to disconnect from remote server.
        """
        # prevent argv IndexError
        argv += [None, None]

        # session save [<FILE>]
        if argv[1] == 'save':
            if argv[2] == '-f':
                path = argv[3]
                ask_confirmation = False
            else:
                path = argv[2]
                ask_confirmation = True
            session.dump(path, ask_confirmation=ask_confirmation)
            path = session.File if path is None else path
            session.File = path
            print("[*] Session saved into %r" % path)
        # session load [<FILE>]
        elif argv[1] == 'load':
            try:
                session.update(argv[2], update_history=True)
                print("[#] Session file correctly loaded")
            except:
                print("[#] Could not load session file")
                raise
        # session diff [<FILE>]
        elif argv[1] == 'diff':
            session.diff(argv[2], display_diff=True)
        # session upgrade
        elif argv[1] == 'upgrade':
            if "id" in session.Compat:
                print("[*] You are about to upgrade phpsploit session.")
                print("[*] Please ensure that you have correctly upgraded")
                print("[*] the remote backdoor into target URL.")
                print("[*] After session upgrade, phpsploit assumes that")
                print("[*] an up-to-date backdoor is active on $TARGET.")
                cancel = ui.input.Expect(False)
                if not cancel("Do you really want to upgrade session now ?"):
                    session.Compat = {}
                    print("[*] Session correctly upgraded")
                else:
                    print("[-] Session upgrade aborted")
            else:
                print("[-] Session already up-to-date")
        # sesion [<FILE>]
        else:
            print(session(argv[1]))

    #################
    # COMMAND: lrun #
    def do_lrun(self, argv):
        """Execute client-side shell command

        SYNOPSIS:
            lrun command [arg1 [arg2 [...] ] ]

        DESCRIPTION:
                Execute a shell command in your own operating system.
                This command works like the `exec` command in unix
                shells.

                NOTE: This core command shouldn't be confused with the
                `run` plugin, which does the same thing in the
                remotely exploited system.

        EXAMPLES:
            > lrun ls -la /
            > lrun htop
        """
        if len(argv) == 1:
            self.interpret("help lrun")
            return False

        cmd = " ".join(argv[1:])
        tmpfile = Path()
        postcmd = "\nret=$?; pwd >'%s' 2>&1; exit $ret" % tmpfile
        ret = os.system(cmd + postcmd) >> 8
        if os.stat(tmpfile).st_size > 0:
            os.chdir(tmpfile.read())
        return ret

    ###################
    # COMMAND: source #
    def do_source(self, argv):
        """Execute a phpsploit script file

        SYNOPSIS:
            source [OPTIONS] <LOCAL_FILE>

        DESCRIPTION:
            Read [LOCAL_FILE] and executes the statements
            contained therein. As if each line was a phpsploit
            command.

        OPTIONS:
            -e
                Abort file sourcing as soon as a command
                fails (aka, returns nonzero), and return
                the code returned by the command which failed.

        EXAMPLES:
            > source /tmp/spl01t-script.phpsploit
              - Run the given script file's content, line by line
        """
        if len(argv) == 2:
            abort_on_error = False
            source_file = argv[1]
        elif len(argv) == 3 and argv[1] == "-e":
            abort_on_error = True
            source_file = argv[2]
        else:
            return self.interpret("help source")

        source_file = utils.path.truepath(source_file)
        with open(source_file, 'r') as file:
            data = file.read()
        return self.interpret(data, fatal_errors=abort_on_error)

    ################
    # COMMAND: set #
    @staticmethod
    def complete_set(text, line, *_):
        """Use settings as `set` completers (case insensitive)"""
        argv = line.split()
        if (len(argv) == 2 and line[-1] == " ") or len(argv) > 2:
            return []
        result = []
        for key in session.Conf.keys():
            if key.startswith(text.upper()):
                result.append(key)
        return result

    @staticmethod
    def do_set(argv):
        """view and edit configuration settings

        SYNOPSIS:
            set [<VAR> [+] ["<VALUE>"]]

        DESCRIPTION:
            Settings are a collection of editable variables that affect
            phpsploit's core behavior.
            - Their value is bound to current session.
            - To permanently change a setting's value at start, it
            must be defined by hand on phpsploit config file.

            > set
              - Display current settings

            > set <STRING>
              - Display settings whose name starts with STRING

            > set <VAR> <VALUE>
              - Assign VALUE to VAR setting (only if it's a valid value)

            > set <VAR> %%DEFAULT%%
              - Reset VAR's default value with '%%DEFAULT%%' magic string

            > set <VAR> "file:///path/to/file"
              - Bind VAR's value to a local file content

            > set <VAR> +
              - Open VAR's value in text editor. This is useful to edit
              values with multiple lines

            > set <VAR> + <LINE>
              - Add LINE to the end of VAR's value

            > set <VAR> + "file:///path/to/file"
              - Re-bind VAR to a local file path.
              Even if path doesn't exist, the setting will take the value of
              the file if it founds it. Otherwise, previous buffer value is
              kept as long as the file path is unreachable

        Defining HTTP Headers:
            You can define custom http request header fields by hand.

            Settings starting with 'HTTP_' are automagically treated as
            HTTP Request Headers values.

            By default, only the "User-Agent" Header is defined. It is bound
            by default to a local file containing common HTTP User Agents.
            (`help set HTTP_USER_AGENT`)

            * Examples:
            > set HTTP_ACCEPT_LANGUAGE "en-CA"
              - Define "Accept-Language" http request header field.
            > set HTTP_ACCEPT_LANGUAGE None
              - Remove HTTP_ACCEPT_LANGUAGE header with magic value 'None'.

        Use `set help <VAR>` for detailed help about a setting.
        """
        # `set [<STRING>]` display concerned settings list
        if len(argv) < 3:
            string = (argv+[""])[1]
            print(session.Conf(string))
            if string not in session.Conf:
                string = "<VAR>"
            print("[*] For detailed help, run `help set %s`" % string)

        # buffer edit mode
        elif argv[2] == "+":
            # `set <VAR> +`: use $EDITOR as buffer viewer in file mode
            if len(argv) == 3:
                # get a buffer obj from setting's raw buffer value
                file_name = argv[1].upper()
                file_ext = "txt"
                setting_obj = session.Conf[argv[1]](call=False)
                if isinstance(setting_obj, datatypes.PhpCode):
                    file_ext = "php"
                elif isinstance(setting_obj, datatypes.ShellCmd):
                    file_ext = "sh"
                buffer = Path(filename="%s.%s" % (file_name, file_ext))
                buffer.write(session.Conf[argv[1]].buffer)
                # try to edit it through $EDITOR, and update it
                # if it has been modified.
                if buffer.edit():
                    session.Conf[argv[1]] = buffer.read()
            # `set <VAR> + "value"`: add value on setting possible choices
            else:
                session.Conf[argv[1]] += " ".join(argv[3:])
        # `set <VAR> "value"`: just change VAR's "value"
        else:
            session.Conf[argv[1]] = " ".join(argv[2:])

    ################
    # COMMAND: env #
    @staticmethod
    def complete_env(text, line, *_):
        """Use env vars as `env` completers (case insensitive)"""
        argv = line.split()
        if (len(argv) == 2 and line[-1] == " ") or len(argv) > 2:
            return []
        result = []
        for key in session.Env:
            if key.startswith(text.upper()):
                result.append(key)
        return result

    @staticmethod
    def do_env(argv):
        """Environment variables handler

        SYNOPSIS:
            env [<NAME> ["<VALUE>"|None]]

        DESCRIPTION:
            Environment variables are meant to store informations
            about remote server state.
            - Their initial value is defined as soon as phpsploit
            opens a remote connection (`exploit`).
            - Plugins can read, write, and create environment variables.

            > env
            - Display all current env vars

            > env <STRING>
            - Display all env vars whose name starts with STRING.

            > env <NAME> <VALUE>
            - Set NAME env variable's value to VALUE.

            > env <NAME> None
            - Remove NAME with 'None' magic string.

        EXAMPLE:
            `PWD` is used to persist 'current working directory' of remote
            target. It allows plugins to use relative path arguments:
            # set PWD to '/var/www':
            > cd /var/www
            # display '/var/www/index.php':
            > cat index.php`

        NOTES:
            - Some envionment variables, such as `PWD` and `WEB_ROOT` are
            crucial for remote session consistency. Be careful before
            manually editing them.

            - Plugins that need to store persistent informations may and
            must use env vars. For example, the `mysql` plugin creates a
            `MYSQL_CRED` environment variable, which contains remote
            database connection credentials. So next calls to `mysql` can be
            used to browse database without providing credentials each time.

            - Unlike Settings (`set` command), env vars are meant to store
            basic strings.
        """
        # `env [<NAME>]`
        if len(argv) < 3:
            if not session.Env:
                print("[-] Must connect to spread env vars (`help exploit`)")
                return False
            print(session.Env((argv + [""])[1]))
            return True
        # `env <NAME> <VALUE>`
        session.Env[argv[1]] = " ".join(argv[2:])
        return True

    ##################
    # COMMAND: alias #
    @staticmethod
    def complete_alias(text, line, *_):
        """autocompletion for `alias` command"""
        argv = line.split()
        if (len(argv) == 2 and line[-1] == " ") or len(argv) > 2:
            return []
        result = []
        for key in session.Alias.keys():
            if key.startswith(text):
                result.append(key)
        return result

    def do_alias(self, argv):
        """Define command aliases

        SYNOPSIS:
            alias [<NAME> ["<VALUE>"|None]]

        DESCRIPTION:
            Command aliases can be defined in order to ease phpsploit
            shell experience.
            Once defined, an alias can be used as if it was a standard
            command, and it's value is interpreted, then suffixed with
            arguments passed to the command line (if any).

            NOTE: This core command works like the unix bash `alias`
            command.

            > alias
              - Display all current command aliases.

            > alias <NAME>
              - Display aliases whose name starts with NAME.

            > alias <NAME> <VALUE>
              - Set NAME alias to the given VALUE.

            > alias <NAME> None
              - Unset NAME command alias.

        BEHAVIOR:
            - Unlike settings, aliases do not provide dynamic random
            values. Setting a value is simply interpreted as a string,
            apart for the special "None" value, which removes the variable.
        """
        if len(argv) < 3:
            # `alias [<PATTERN>]` display concerned settings list
            print(session.Alias((argv+[""])[1]))
        else:
            # `alias <NAME> <VALUE>`
            existed = argv[1] in session.Alias
            session.Alias[argv[1]] = " ".join(argv[2:])
            exists = argv[1] in session.Alias
            if existed and not exists:
                print("[*] `%s` alias correctly deleted." % argv[1])
            elif existed and exists:
                print("[-] `%s` alias correctly overridden." % argv[1])
            elif exists:
                if argv[1] in self.get_names(self, "do_"):
                    print("[-] Warning: %r command overridden"
                          " (run `alias %s None` to unset alias)"
                          % (argv[1], argv[1]))
                elif argv[1] in plugins.keys():
                    print("[-] Warning: %r plugin overridden"
                          " (run `alias %s None` to unset alias)"
                          % (argv[1], argv[1]))


    ##################
    # COMMAND: bind #
    def complete_bind(self, text, line, *_):
        """autocompletion for `bind` command"""
        result = self.completenames(text, line, *_)
        if not result:
            return []
        result = [x for x in result if x != "bind"]
        if tunnel:
            result += plugins.keys()
        return [x for x in list(set(result)) if x.startswith(text)]

    def do_bind(self, argv):
        """attach a command to prompt

        SYNOPSIS:
            bind [<COMMAND>]

        DESCRIPTION:
            Bind phpsploit prompt to COMMAND.
            Every line executed will then be executed as if it was
            the arguments of COMMAND.
            This is useful for plugins like `run` or `mysql`, when you
            are working from them and don't want to re-type the plugin
            name again and again ..

            NOTE: press Ctrl-D or type exit to 'unbind' from current command.

        DEMO:
            phpsploit(127.0.0.1) > run type ls
            ls is /bin/ls
            phpsploit(127.0.0.1) > type ls
            [-] Unknown Command: type
            phpsploit(127.0.0.1) > bind run
            [-] Type exit to leave binded 'run' subshell
            # now shell is bound to `run`, so we just need to execute `type ls`
            phpsploit(127.0.0.1) #run > type ls
            ls is /bin/ls
        """
        if len(argv) != 2 or argv[1] not in self.complete_bind("", ""):
            self.interpret("help bind")
        else:
            self.bind_command = argv[1]
            print("[-] Type exit to leave bound %r subshell" % argv[1])


    ####################
    # COMMAND: backlog #
    def do_backlog(self, argv):
        """open last command output in text editor

        SYNOPSIS:
            backlog [--save <FILE>]

        DESCRIPTION:
            Open last command output with text EDITOR (`help set EDITOR`).
            Ansi terminal colors are automatically stripped from buffer.

        OPTIONS:
            --save <FILE>
                Write previous command's output to the given
                file instead of opening it with $EDITOR.
        """
        if len(argv) == 1:
            backlog = Path()
            backlog.write(self.stdout.backlog, bin_mode=True)
            backlog.edit()
        elif len(argv) == 3 and argv[1] == "--save":
            Path(argv[2]).write(self.stdout.backlog)
        else:
            self.interpret("help backlog")


    #################
    # COMMAND: help #
    def complete_help(self, text, line, *_):
        """Use settings as `set` completers (case insensitive)"""
        argv = line.split()
        if argv[:2] == ["help", "set"]:
            if (len(argv) == 2 and line[-1] == " ") \
                    or (len(argv) == 3 and line[-1] != " "):
                return [x for x in session.Conf if x.startswith(text)]
            if len(argv) > 2 or line[-1] == " ":
                return []
        return self.completenames(text, line, *_)

    def do_help(self, argv):
        """Show commands help

        SYNOPSIS:
            help
            help <COMMAND>
            help set <SETTING>

        DESCRIPTION:
            Get help for any core command or plugin.

            If called without arguments, a list of available commands,
            plugins, and aliases is displayed.
            Otherwise, detailed help of given command is shown.

            * NOTE: plugins are only listed after running `exploit`

        EXAMPLES:
            > help
              - List available commands, plugins, and aliases
            > help help
              - Get detailed help on `help` command
            > help exit
              - Display the help for the `exit` command
            > help set BACKDOOR
              - Display help about the "BACKDOOR" setting
        """
        def get_doc(cmd):
            """get lines from `cmd` docstring"""
            doc = ""
            if hasattr(self, "do_" + cmd):
                doc = getattr(self, "do_" + cmd).__doc__
            elif cmd in plugins:
                doc = plugins[cmd].help
                if doc.strip():
                    doc += "\nPLUGIN LOCATION:\n    " + plugins[cmd].path
            return doc.strip().splitlines()

        def get_description(doc_lines):
            """get formatted command help description"""
            if doc_lines:
                return doc_lines[0].strip()
            return colorize("%Yellow", "No description")

        def doc_help(doc_lines):
            """print formated command's docstring"""
            # reject empty docstrings (description + empty line)
            if len(doc_lines) < 2:
                return False
            doc_lines.pop(0)  # remove the description line
            while not doc_lines[0].strip():
                doc_lines.pop(0)  # remove heading empty lines
            # remove junk leading spaces (due to python indentation)
            trash = len(doc_lines[0]) - len(doc_lines[0].lstrip())
            doc_lines = [line[trash:].rstrip() for line in doc_lines]
            # hilight lines with no leading spaces (man style)
            result = ""
            for line in doc_lines:
                if line == line.lstrip():
                    line = colorize("%BoldWhite", line)
                elif line.startswith("    * "):
                    line = colorize("    * ", "%Yellow", line[6:])
                elif line.startswith("    > "):
                    line = colorize("    > ", "%Cyan", line[6:])
                elif line.startswith("    # "):
                    line = colorize("%Dim", line)
                elif line.startswith("    -") and line[5] != " ":
                    line = colorize("%Green", line)
                result += line + "\n"
            print(result)
            return True

        # help set <VAR>
        if len(argv) >= 3 and argv[1] == "set":
            var = argv[2].upper()
            try:
                doc = getattr(session.Conf, var).docstring
            except KeyError:
                print("[-] %s: No such setting (run `set` to list settings)" \
                        % var)
                return False
            print("\n[*] Help for '%s' setting\n" % var)
            return doc_help(doc.splitlines())

        # help <COMMAND>
        if len(argv) >= 2:
            doc = get_doc(argv[1])
            if doc:
                print("\n[*] %s: %s\n" % (argv[1], get_description(doc)))
                # call help_COMMAND() or fallback to COMMAND's docstring
                help_method = getattr(self, "help_" + argv[1], None)
                if callable(help_method):
                    getattr(self, 'help_' + argv[1])()
                else:
                    if not doc_help(doc):
                        return False
                if argv[1] in session.Alias:
                    print("[-] Warning: %r has been aliased "
                          "(run `alias %s` for + infos)"
                          % (argv[1], argv[1]))
                return True
            # fallback to alias display
            elif argv[1] in session.Alias:
                return self.interpret("alias %s" % argv[1])
            print(self.nohelp % argv[1])
            return False

        # help
        core_commands = self.get_names(self, "do_")
        full_help = [('Core Commands', core_commands)]
        max_len = max(13, len(max(core_commands, key=len)))
        # add plugins if connected to target
        if tunnel:
            for category in plugins.categories():
                items = [p for p in plugins.values() if p.category == category]
                items = [p.name for p in items]
                # rescale max_len in case of longer plugin names
                max_len = max(max_len, len(max(items, key=len)))
                full_help += [(category + " Plugins", items)]
        # adapt max_len if there are command aliases
        aliases = list(session.Alias.keys())
        if aliases:
            max_len = max(max_len, len(max(aliases, key=len)))
            full_help += [("Command Aliases", aliases)]
        # print full_help, group by group
        cmd_col = ' ' * (max_len - 5)
        for grp_name, grp_cmdlist in full_help:
            underline = '=' * len(grp_name)
            if grp_name == "Command Aliases":
                print("\n" + grp_name + "\n" + underline + "\n"
                      "    Alias  " + cmd_col + "Value\n"
                      "    -----  " + cmd_col + "-----")
            else:
                print("\n" + grp_name + "\n" + underline + "\n"
                      "    Command" + cmd_col + "Description\n"
                      "    -------" + cmd_col + "-----------")
            grp_cmdlist.sort()
            for cmd_name in grp_cmdlist:
                spacing = ' ' * (max_len - len(cmd_name) + 2)
                if grp_name == "Command Aliases":
                    description = session.Alias[cmd_name]
                else:
                    description = get_description(get_doc(cmd_name))
                print("    " + cmd_name + spacing + description)
            print('')

    # pylint: disable=invalid-name
    @staticmethod
    def except_OSError(exception):
        """Fix OSError args, removing errno, and adding filename"""
        if isinstance(exception.errno, int):
            exception.args = (exception.strerror,)
        if exception.filename is not None:
            exception.args += ("«{}»".format(exception.filename),)
        return exception

    @staticmethod
    def debug_cmdrepr(argv):
        """Returns a nice representation of given command arguments
        """
        cmdrepr = []
        for arg in argv:
            if not isinstance(arg, str):
                continue
            argrepr = repr(arg)
            sep = argrepr[0], argrepr[-1]
            argrepr = argrepr[1:-1].join(colorize("%DimCyan", "%Reset"))
            cmdrepr.append(sep[0] + argrepr + sep[1])
        args = " ".join(cmdrepr)
        return colorize("%BoldCyan", "CMD(", "%Reset", args, "%BoldCyan", ")")
