<?

// fileAccess($abspath, $mode) (type => boolean):
//      Check if $abspath has $mode permission.
//      
//      $abspath (string):
//          This variable must link to a regular file.
//      $mode (char):
//          Mode should be 'r' to test read access, and 'w'
//          to check write access.
//
// EXAMPLE:
//      >>> fileAccess("/etc/passwd", 'r')
//      True
//      >>> fileAccess("/etc/passwd", 'w')
//      False
//
// TODO: It will be smart if the function could restore atime
// (access time) on unix systems after testing for stealth purposes.

function fileAccess($abspath, $mode)
{
    // Assuming cases where user wants to check write access, he
    // will then pass 'w' as mode argument. Therefore, we just can't
    // allow this mode internally, because doing a fopen() with 'w' mode
    // will empty the file in case of success, which is clearly stupid.
    if ($mode != 'r')
        $mode = 'a';

    // fopen() the given file path and return True in case of success
    if ($h = @fopen($abspath, $mode))
    {
        fclose($h);
        return (True);
    }
    else
        return (False);
}

?>
