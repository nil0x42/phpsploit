<?

// dirAccess($abspath, $mode) (type => boolean):
//      Check if $abspath directory has $mode permission.
//      
//      $abspath (string):
//          This variable must refer to an exsting directory.
//      $mode (char):
//          Mode should be 'r' to test read access, and 'w'
//          to check write access.
//
// EXAMPLE:
//      >>> dirAccess("/etc/", 'r')
//      True
//      >>> dirAccess("/etc/", 'w')
//      False
//
// TODO: It will be smart if the function could restore atime
// (access time) on unix systems after testing for stealth purposes.

function dirAccess($abspath, $mode)
{
    if ($mode == 'r')
    {
        if ($h = @opendir($abspath))
        {
            closedir($h);
            return (True);
        }
        else
            return (False);
    }
    elseif ($mode == 'w' || $mode == 'a')
    {
        $old_mtime = @filemtime($abspath);
        $old_atime = @fileatime($abspath);
        $rand = $abspath . uniqid('/pspapi_');
        if ($h = @fopen($rand, 'a'))
        {
            @fclose($h);
            $result = True;
        }
        else
        {
            $result = False;
        }
        @unlink($rand);
        @touch($abspath, $old_mtime, $old_atime);
        return ($result);
    }
    else
        return (False);
}

?>
