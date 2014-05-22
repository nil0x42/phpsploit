# PhpSploit framework's user configuration directory
----------------------------------------------------


./config file
=============

The ./config file is automatically sourced at framework initialisation,
and is the correct way to configure special behaviors at start, such
as defining custom values for settings.
The ./config file is interpreted line by line, as if each line had been
typed in the framework interface. For example, is you want to overwrite
the PASSKEY setting's default value, just add the following line to the
configuration file:
    > set PASSKEY "myPassKey"


./plugins directory
===================

This directory must be used for user specific plugins.
It works exactly the same way as phpsploit's plugins directory.

* Structure convention:

First level directories are considered as category names, while their
childs (second level directories) are the plugin names.

Each plugin contains at least a 'plugin.py' file.

---------------------------

plugins/
 +-- file_system/
      +-- shred/
      |    +-- plugin.py
      |    +-- payload.php
      +-- top/
      |    +-- plugin.py
      |    +-- payload.php
 +-- personnal/
      +-- sendBot/
      |    +-- plugin.py
      |    +-- payload.php
 +-- testing/
      +-- netscan
      |    +-- plugin.py
      |    +-- payload.php

---------------------------

In the plugins tree below, two personnal plugins have been added in the
file system category (which is standard), while both `personnal` and
`testing` categories contains one new plugin each.
