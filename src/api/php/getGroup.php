<?

// getGroup($abspath) (type => string):
//      Return group owner of the given file path.
//
//      If the group owner of the file could not be determined,
//      the string "?" is returned as a fallback value.
//
//      $abspath (string):
//          This variable should be an existing absolute file path

function getGroup($abspath)
{
    if (function_exists('posix_getgrgid'))
    {
        $gid = @filegroup($abspath);
        $grp = @posix_getgrgid($gid);
        if (@is_string($grp['name']) && !@empty($grp['name']))
            return ($grp['name']);
    }
    return ("?");
}

?>
