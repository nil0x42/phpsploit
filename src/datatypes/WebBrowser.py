import webbrowser
from ui.color import colorize


class WebBrowser(str):
    """Web browser object. (extends str, and users webbrowser lib);

    Takes the name of an available web browser in the current system.

    >>> browser = WebBrowser('firefox')
    >>> browser()
    "/usr/bin/firefox"
    >>> browser.open('http://www.google.com/')
    True

    """
    def __new__(cls, name):
        # a boring Mas OS/X case ..
        blacklist = ['macosx']

        lst = [x for x in webbrowser._browsers.keys() if x not in blacklist]
        lst.append("disabled")
        lst_repr = repr(lst)[1:-1]

        if len(lst) < 2 or name == "disabled":
            if name not in lst + ["", "default"]:
                raise ValueError("Can't bind to «%s». Valid choices: %s"
                        % (name, lst_repr))
            return str.__new__(cls, "disabled")

        try:
            if name.lower() in ["", "default"]:
                name = webbrowser.get().name
            else:
                webbrowser.get(name)
        # another boring Mac OS/X case ..
        except AttributeError:
            return str.__new__(cls, "default")
        except:
            raise ValueError("Can't bind to «%s». Valid choices: %s"
                    % (name, lst_repr))
        return str.__new__(cls, name)

    def _raw_value(self):
        return super().__str__()

    def __call__(self):
        return self._raw_value()

    def __str__(self):
        val = self._raw_value()
        if val == 'disabled':
            return colorize('%Red', val)
        elif val:
            return colorize('%Cyan', val)
        else:
            return colorize('%Cyan', "default")

    def open(self, url):
        val = self._raw_value()
        if val == "disabled":
            print("[-] BROWSER is disabled, open the following URL manually:")
            print("[-]   %s" % url)
        else:
            browser = webbrowser.get(self._raw_value())
            # try to open url in new browser tab
            return browser.open_new_tab(url)
