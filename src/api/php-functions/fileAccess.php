<?

// fileAccess($abspath, $mode) (type => boolean):
//      Check if $abspath has $mode permission.
//      
//      $abspath (string):
//          This variable must link to a regular file.
//      $mode (char):
//          'r': Check if readable
//          'w': Check if writable
//          'x': Check if executable
//
// EXAMPLE:
//      >>> fileAccess("/etc/passwd", 'r')
//      True
//      >>> fileAccess("/etc/passwd", 'w')
//      False

function fileAccess($abspath, $mode)
{
    // Assuming cases where user wants to check write access, he
    // will then pass 'w' as mode argument. Therefore, we just can't
    // allow this mode internally, because doing a fopen() with 'w' mode
    // will empty the file in case of success, which is clearly stupid.
    if ($mode != 'r' && $mode != 'x')
        $mode = 'a';

    if ($mode == 'x')
        return @is_executable($abspath);

    // fopen() the given file path and return True in case of success
    $old_mtime = @filemtime($abspath);
    $old_atime = @fileatime($abspath);
    if ($h = @fopen($abspath, $mode))
    {
        fclose($h);
        @touch($abspath, $old_mtime, $old_atime);
        return (True);
    }
    else
        return (False);
}

?>
