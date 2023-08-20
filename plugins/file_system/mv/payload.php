<?


$src = $PHPSPLOIT['SRC'];
$dst = $PHPSPLOIT['DST'];


// check source file access and get source file's buffer
if (!@file_exists($src))
    return error("cannot stat '%s': No such file or directory", $src);
if (!@is_file($src))
    return error("cannot move '%s': Not a regular file", $src);
if (!is_readable($src))
    return error("cannot open '%s' for reading: Permission denied", $src);

// if dst is a directory, append source's basename to it.
if (@is_dir($dst)) {
    if (substr($dst, -1) != $PHPSPLOIT['PATH_SEP'])
        $dst .= $PHPSPLOIT['PATH_SEP'];
    $dst .= basename($src);
}

// if dst is a directory, append source's basename to it.
$dir = dirname($dst);

if (@is_dir($dir)) {
    if (is_writable($dir)) {
        if (!@file_exists($dst)) {
            @rename($src, $dst);
        }else{
            return error("cannot move '%s': File exists", $dir);
        }
    } else {
        return error("cannot create regular file '%s': Permission denied", $dst);
    }
}
return array($src, $dst);
