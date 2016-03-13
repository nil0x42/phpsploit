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
        fmt = ", ".join(lst)
        try:
            if name.lower() in ["", "default"]:
                name = webbrowser.get().name
            else:
                webbrowser.get(name)
        # another boring Mac OS/X case ..
        except AttributeError:
            return str.__new__(cls, "default")
        except:
            raise ValueError("Can't bind to «%s». Try one of %s"
                    % (name, fmt))
        return str.__new__(cls, name)

    def _raw_value(self):
        return super().__str__()

    def __call__(self):
        return self._raw_value()

    def __str__(self):
        if self:
            return colorize('%Cyan', self._raw_value())
        else:
            return colorize('%Cyan', "default")

    def open(self, url):
        browser = webbrowser.get(self._raw_value())
        # try to open url in new browser tab
        return browser.open_new_tab(url)
