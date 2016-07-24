<?

// getPerms($abspath, $perms_type) (type => string):
//      Returns the `human permissions string` of the given
//      file path.
//
//      $perms_type (string) (default="unix")
//          - If $perms_type is "unix", then a full permissions
//          string like '-rwxr-xr-x' is returned.
//          - Otherwise, the returned string will be related to
//          current access of the file for user, in the following
//          format: 'drwx'. This format tells if we actually can
//          read/write/execute the file, by stupidly testing
//          accesses.
//
//      $abspath (string):
//          This variable should be an existing absolute file path

!import(can_change_mtime)
!import(fileAccess)
!import(dirAccess)

function getPerms($abspath, $perms_format="unix")
{
    global $PHPSPLOIT;
    $perms = @fileperms($abspath);

    // FILE TYPES:
    // s: socket
    // -: regular file
    // b: special file
    // d: directory
    // c: special char
    // p: fifo pipe
    // u: unknown type
    if (($perms & 0xC000) == 0xC000)
        $type = 's';
    elseif (($perms & 0xA000) == 0xA000)
        $type = 'l';
    elseif (($perms & 0x8000) == 0x8000)
        $type = '-';
    elseif (($perms & 0x6000) == 0x6000)
        $type = 'b';
    elseif (($perms & 0x4000) == 0x4000)
        $type = 'd';
    elseif (($perms & 0x2000) == 0x2000)
        $type = 'c';
    elseif (($perms & 0x1000) == 0x1000)
        $type = 'p';
    else
        $type = 'u';

    if ((substr($abspath, -3) == $PHPSPLOIT['PATH_SEP'] . '..') ||
        (substr($abspath, -2) == $PHPSPLOIT['PATH_SEP'] . '.'))
        $type = 'd';

    if ($perms_format == 'unix'){
        $info = "";
        // myself
        $info .= (($perms & 0x0100) ? 'r' : '-');
        $info .= (($perms & 0x0080) ? 'w' : '-');
        $info .= (($perms & 0x0040) ?
                    (($perms & 0x0800) ? 's' : 'x' ) :
                    (($perms & 0x0800) ? 'S' : '-'));
        // my group
        $info .= (($perms & 0x0020) ? 'r' : '-');
        $info .= (($perms & 0x0010) ? 'w' : '-');
        $info .= (($perms & 0x0008) ?
                    (($perms & 0x0400) ? 's' : 'x' ) :
                    (($perms & 0x0400) ? 'S' : '-'));
        // others
        $info .= (($perms & 0x0004) ? 'r' : '-');
        $info .= (($perms & 0x0002) ? 'w' : '-');
        $info .= (($perms & 0x0001) ?
                    (($perms & 0x0200) ? 't' : 'x' ) :
                    (($perms & 0x0200) ? 'T' : '-'));}

    else
    {
        $Rperm = (($perms & 0x0004) ? 'r' : '-');
        $Wperm = (($perms & 0x0002) ? 'w' : '-');
        $Xperm = (($perms & 0x0001) ?
                    (($perms & 0x0200) ? 't' : 'x' ) :
                    (($perms & 0x0200) ? 'T' : '-'));

        if ($type == '-')
        {
            if (fileAccess($abspath, 'r'))
                $Rperm = 'r';
            else
                $Rperm = '-';

            if (can_change_mtime($abspath))
            {
                if (fileAccess($abspath, 'w'))
                    $Wperm = 'w';
                else
                    $Wperm = '-';
            }
        }
        elseif ($type == 'd')
        {
            if (dirAccess($abspath, 'r'))
            {
                $Rperm = 'r';
                $Xperm = 'x';
            }
            else
            {
                $Rperm = '-';
                $Xperm = '-';
            }

            if (can_change_mtime($abspath))
            {
                if (dirAccess($abspath, 'w'))
                    $Wperm = 'w';
                else
                    $Wperm = '-';
            }
        }
        $info = $Rperm . $Wperm . $Xperm;
    }

    return ($type . $info);
}

?>
