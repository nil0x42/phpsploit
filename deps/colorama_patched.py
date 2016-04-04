"""
Monkeypatch colorama to support a few additional text styles

'Tale' mud driver, mudlib and interactive fiction framework
Copyright by Irmen de Jong (irmen@razorvine.net)
"""
from __future__ import absolute_import, print_function, division, unicode_literals
import colorama
import colorama.ansi
import colorama.winterm
import colorama.ansitowin32
import colorama.win32


# patch in a few extra ansi styles
if not hasattr(colorama.ansi.AnsiStyle, "ITALIC"):
    colorama.ansi.AnsiStyle.ITALIC = 3
    colorama.ansi.AnsiStyle.UNDERLINED = 4
    colorama.ansi.AnsiStyle.BLINK = 5
    colorama.ansi.AnsiStyle.REVERSEVID = 7
    if colorama.__version__ >= "0.3.4":
        colorama.ansi.Style = colorama.Style = colorama.ansi.AnsiStyle()
    else:
        colorama.ansi.Style = colorama.Style = colorama.ansi.AnsiCodes(colorama.ansi.AnsiStyle)

# Patch in a trick to use reverse video on windows console (where REVERSEVID doesn't work natively)
if colorama.win32.windll is not None and not hasattr(colorama.ansitowin32.AnsiToWin32, "style_reverse_vid"):
    class MonkeypatchedAnsiToWin32(colorama.ansitowin32.AnsiToWin32):
        def get_win32_calls(self):
            result = super(MonkeypatchedAnsiToWin32, self).get_win32_calls() or {}
            result[colorama.ansi.AnsiStyle.REVERSEVID] = (self.style_reverse_vid, )
            return result

        def style_reverse_vid(self, style=None, on_stderr=False):
            # Reverse-video style doesn't seem to work on windows, so we simulate it:
            # flip foreground and background colors.
            term = colorama.ansitowin32.winterm
            term._fore, term._back = term._back, term._fore
            term.set_console(on_stderr=on_stderr)

    colorama.win32.COORD = colorama.win32.wintypes._COORD
    import colorama.initialise
    colorama.ansitowin32.AnsiToWin32 = MonkeypatchedAnsiToWin32
    colorama.initialise.AnsiToWin32 = colorama.ansitowin32.AnsiToWin32
    colorama.AnsiToWin32 = colorama.ansitowin32.AnsiToWin32


from colorama import *

if __name__ == "__main__":
    colorama.init()
    print("\x1b[1;1H\x1b[2J------------colorama test (clear screen)-------------")
    print(colorama.Style.BRIGHT + "bright" + colorama.Style.RESET_ALL)
    print(colorama.Style.UNDERLINED + "underlined" + colorama.Style.RESET_ALL)
    print(colorama.Style.BLINK + "blink" + colorama.Style.RESET_ALL)
    print(colorama.Style.ITALIC + "italic" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + colorama.Back.RED + "yellow on red" + colorama.Style.RESET_ALL)
    print(colorama.Style.REVERSEVID + "reversevid" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + colorama.Back.RED + colorama.Style.REVERSEVID + "yellow on red, reversed" + colorama.Style.RESET_ALL)
