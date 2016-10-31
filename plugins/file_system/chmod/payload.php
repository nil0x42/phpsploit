<?php

if (!@file_exists($PHPSPLOIT['FILE']))
    return error("%s: No such file or directory", $PHPSPLOIT['FILE']);

if (!@chmod($PHPSPLOIT["FILE"], $PHPSPLOIT["MODE"]))
    return error("%s: Permission denied", $PHPSPLOIT['FILE']);

return 'ok';

?>
