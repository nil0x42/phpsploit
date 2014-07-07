<?

!import(dirAccess)

// If directory has read access, just return success.
if (dirAccess($PHPSPLOIT['DIR'], 'r'))
    return 'ok';
// Otherwise, determine the error message to return.
else
{
    if (@file_exists($PHPSPLOIT['DIR']))
    {
        if ((@fileperms($PHPSPLOIT['DIR']) & 0x4000) == 0x4000)
            return error("%s: Permission denied", $PHPSPLOIT['DIR']);
        else
            return error("%s: Not a directory", $PHPSPLOIT['DIR']);
    }
    else
        return error("%s: No such file or directory", $PHPSPLOIT['DIR']);
}

?>
