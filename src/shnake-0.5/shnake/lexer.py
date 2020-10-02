"""Shnake's pyparsing based shell lexer

Based on the awesome pyparsing library, the Lexer class intends to provide
a powerful bash-like string lexer.

"""

import re

__author__ = "nil0x42 <http://goo.gl/kb2wf>"


class Lexer:
    r"""Bash-like string lexer based on pyparsing.

    It implements a very basic bash inspired lexer that supports
    multicommands, logical operators, pipes, and standard file
    descriptor redirection.

    Its __init__() method takes a string as argument. If the syntax
    if correct, a list() if then returned.
    A list() is a pipeline, aka an instruction block.

    Case study:
    -----------
    >>> lex = Lexer()
    >>> lex("ls -la /tmp 2>&1 && echo foo'bar'\ ")
    [["ls", "-la", "/tmp", (2, ">", 1)], "&&", ["echo", "foobar "]]

    The example above shows a basic case of string lexing.
    Here, the pipeline (aka the main list()) returned: list, str, list;
    each sub list is a single command, and they are separated by the
    "&&" logical operator. It makes easy post processing for binary
    conditions.
    Also, note that the first command's redirection instruction had
    been parsed as a tuple(), facilitating post processing adaptation.

    """

    def __init__(self):
        from pyparsing import (ParserElement, StringEnd, LineEnd, Literal,
                               pythonStyleComment, ZeroOrMore, Suppress,
                               Optional, Combine, OneOrMore, Regex, oneOf,
                               QuotedString, Group, ParseException)

        ParserElement.setDefaultWhitespaceChars("\t ")

        EOF = StringEnd()
        EOL = ~EOF + LineEnd()  # EOL must not match on EOF

        escape = Literal("\\")
        comment = pythonStyleComment
        junk = ZeroOrMore(comment | EOL).suppress()

        # word (i.e: single argument string)
        word = Suppress(escape + EOL + Optional(comment)) \
            | Combine(OneOrMore(
                escape.suppress() + Regex(".") |
                QuotedString("'", escChar='\\', multiline=True) |
                QuotedString('"', escChar='\\', multiline=True) |
                Regex("[^ \t\r\n\f\v\\\\$&<>();\\|\'\"`]+") |
                Suppress(escape + EOL)))

        # redirector (aka bash file redirectors, such as "2>&1" sequences)
        fd_src = Regex("[0-2]").setParseAction(lambda t: int(t[0]))
        fd_dst = Suppress("&") + fd_src
        # "[n]<word" || "[n]<&word" || "[n]<&digit-"
        fd_redir = (Optional(fd_src, 0) + Literal("<")
                    | Optional(fd_src, 1) + Literal(">")) + \
                   (word | (fd_dst + Optional("-")))
        # "&>word" || ">&word"
        obj = (oneOf("&> >&") + word)
        full_redir = obj.setParseAction(lambda t: ("&", ">", t[-1]))
        # "<<<word" || "<<[-]word"
        here_doc = Regex("<<(<|-?)") + word
        # "[n]>>word"
        add_to_file = (Optional(fd_src | Literal("&"), 1)
                       + Literal(">>")
                       + word)
        # "[n]<>word"
        fd_bind = Optional(fd_src, 0) + Literal("<>") + word

        obj = (fd_redir | full_redir | here_doc | add_to_file | fd_bind)
        redirector = obj.setParseAction(tuple)

        # single command (args/redir list)
        command = Group(OneOrMore(redirector | word))

        # logical operators (section splits)
        semicolon = Suppress(";") + junk
        connector = (oneOf("&& || |") + junk) | semicolon

        # pipeline, aka logical block of interconnected commands
        pipeline = junk + Group(command +
                                ZeroOrMore(connector + command) +
                                Optional(semicolon))

        # define object attributes
        self.LEXER = pipeline.ignore(comment) + EOF
        self.parseException = ParseException

    def __call__(self, string, line=1):
        try:
            result = self.LEXER.parseString(string)

        except self.parseException as error:
            index = error.loc

            try:
                char = string[index]
            except:
                if string.strip() == "\\":
                    err = r"unexpected EOF after escaped newline '\\n'"
                    raise SyntaxWarning(err)
                return []

            if char in "\"'":
                err = "unexpected EOF while looking for matching %r"
                raise SyntaxWarning(err % char)

            elif (index + 1) == len(string) and char == "\\":
                err = r"unexpected EOF after escaped newline '\\n'"
                raise SyntaxWarning(err)

            elif string[index:index+2] in ["&&", "||"]:
                raise SyntaxWarning("unexpected end of file")

            else:
                err = "unexpected token %r "
                # err += str(error)[str(error).find("("):]
                err += str(error)[str(error).rfind("(at char "):]
                try:
                    lineNr = int(re.findall(r"line:(\d+)", err)[0])
                    lineNr += line - 1
                    err = re.sub(r"line:(\d+)", "line:"+str(lineNr), err)
                except:
                    pass
                raise SyntaxError(err % char)

            raise error

        # help(result)
        # for command in result[0]:
        #     print (x)
        # return list(result[0])

        return [list(command) for command in list(result[0])]

lex = Lexer()
