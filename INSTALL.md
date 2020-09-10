## Quick Start

```sh
git clone https://github.com/nil0x42/phpsploit
cd phpsploit/
pip3 install -r requirements.txt
./phpsploit -ie 'help help'
```


### Platform

Compatible with GNU/Linux (and maybe Mac OS/X)
> _Tested on debian, kali, archlinux, and fedora_


### Python Version

Compatible with python >= 3.5
> _(Mostly tested with python 3.5)_


### Dependencies _(included in ./deps from now)_

*   **phpserialize**
    `import phpserialize`
    Needed to communicate between Python and PHP remote execution

*   **pyparsing**
    `import pyparsing`
    A dependency of `shnake`. Used to parse command-line input

*   **PySocks**
    `import socks, sockshandler`
    Needed by the PROXY setting to support socks4/5 proxy types


### Optional dependencies

*   **pygments**
    `import pygments`
    Enable php code syntax coloration

*   **bpython**
    `import bpython`
    Enhanced python console for use with `corectl python-console`

*   **IPython**
    `import IPython`
    Enhanced python console for use with `corectl python-console`
