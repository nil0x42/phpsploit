<?

// getOwner($abspath) (type => string):
//      Return the user name that owns the given $abspath.
//
//      If the owner of the file could not be determined,
//      the string "?" is returned as a fallback value.
//
//      $abspath (string):
//          This variable should be an existing absolute file path

function getOwner($abspath)
{
    if (function_exists('posix_getpwuid'))
    {
        $uid = @filegroup($abspath);
        $usr = @posix_getpwuid($uid);
        if (@is_string($usr['name']) && !@empty($usr['name']))
            return ($usr['name']);
    }
    return ("?");
}

?>
