<?

$src = $PHPSPLOIT["FILE"];

if (!@file_exists($src))
    return error("cannot remove '%s': No such file or directory", $src);

if ((@fileperms($src) & 0x8000) != 0x8000)
    return error("cannot remove '%s': Not a file", $src);

if (@unlink($src) === FALSE)
    return error("cannot remove '%s': Permission denied", $src);

return "ok";

?>
