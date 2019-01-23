### Platform ###

Compatible with GNU/Linux, and maybe Mac OS/X.
*Tested with debian, kali, archlinux, and fedora*


### Python Version ###

Compatible with python >= 3.4
*(Mostly tested with python 3.5)*


### Dependencies (included in ./deps from now) ###

* phpserialize:
    `import phpserialize`
    Needed to communicate between Python and PHP remote execution

* shnake:
    `import shnake`
    The base library for phpsploit command-line interface

* pyparsing:
    `import pyparsing`
    A dependency of `shnake`. Used to parse command-line input

* PySocks:
    `import socks, sockshandler`
    Needed by the PROXY setting to support socks4/5 proxy types


### Optional dependencies ###

> * readline:
>     `import readline`
>     Autocompletion and history surf in the interface.
>     (DISABLED: readline is already in standard library)

* pygments:
    `import pygments`
    Enable php code syntax coloration

* bpython:
    `import bpython`
    Enhanced python console for use with `corectl python-console`

* IPython:
    `import IPython`
    Enhanced python console for use with `corectl python-console`
