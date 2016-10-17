<?php

$mtime = @filemtime($PHPSPLOIT["FILE"]);

// If the file does not exists, the file could be edited for
// creation anyway, so we inform plugin that file does not exists.
if (!@file_exists($PHPSPLOIT['FILE']))
    return "NEW_FILE";

// If the path is not a regular file, throw error.
if ((@fileperms($PHPSPLOIT['FILE']) & 0x8000) != 0x8000)
    return error("%s: Not a file", $PHPSPLOIT['FILE']);

// Get file contents, or throw error (unreadable file).
if (($data = @file_get_contents($PHPSPLOIT['FILE'])) === False)
    return error("%s: Read permission denied", $PHPSPLOIT['FILE']);

// Return the file data (in base64 format)
return array($mtime, base64_encode($data));

?>
