### PhpSploit: *Advanced post-exploitation framework* ###

PhpSploit is a **remote control** framework, aiming to provide a **stealth**
interactive shell-like connection over HTTP between client and web server.

It is a post-exploitation tool capable to maintain access to a
compromised web server for **privilege escalation** purposes.

#### Overview ####

The PhpSploit framework replaces classic PHP backdoor like "c99.php".

    - Ultra small Backdoor (~ 50 chars)
    - Nearly invisible by log analysis
    - Bypass PHP servers wich disables remote execution.
    - Supports GET and POST, independently from the backdoor.

#### Example usage ####

phpspoit \> **infect**
  
```py
[*] The following payload must be inserted in the target web page.
[*] Then adjust the TARGET setting to it in order to start the remote shell

==========================================
<?php @eval($_SERVER['HTTP_PHPSPL01T']);?>
==========================================`
```

**__phpsploit__** **>**
**__phpsploit__ >**

### Advanced Features ###

Very easy to get started, it is also highly configurable, and is designed
to meet all the needs to web security experts.

* Advanced tunnel based payload execution:


    - Uses advanced HTTP Headers filling methods.
    - Provides multi-paradygm payload compression.
    - Tu


The PhpSploit framework takes control over a remote PHP web server.
It replaces classic 

Phpsploit simulates a remote shell access through PHP.

It's first design
