<?

!import(dirAccess)

$dir = $PHPSPLOIT["DIR"];

if (!@file_exists($dir))
    return error("failed to remove '%s': No such file or directory", $dir);

if ((@fileperms($dir) & 0x4000) != 0x4000)
    return error("failed to remove '%s': Not a directory", $dir);

if (@rmdir($dir) === FALSE)
{
    if (dirAccess($dir, 'r'))
        return error("failed to remove '%s': Directory not empty", $dir);
    return error("failed to remove '%s': Permission denied", $dir);
}

?>
