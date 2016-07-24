<?

// can_change_mtime($path) (type => bool):
//      check if mtime can be arbitrarly changed

function can_change_mtime($path)
{
    $old_mtime = @filemtime($path);
    $old_atime = @fileatime($path);
    return @touch($path, $old_mtime, $old_atime);
}

?>
