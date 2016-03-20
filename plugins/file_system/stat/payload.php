<?php

$path = $PHPSPLOIT['FILE'];
$follow_links = $PHPSPLOIT['FOLLOW_LINKS'];

if (!@file_exists($path) && !@is_link($path))
    return error("%s: No such file or directory", $PHPSPLOIT['FILE']);

// r['file_repr']
$file_repr = "'$path'";
if (!$follow_links && ($link_path = @readlink($path)))
        $file_repr .= " -> '" . $link_path . "'";

if ($follow_links && is_link($path))
{
    $path = realpath($path);
    if (!@file_exists($path))
        return error("%s: No such file or directory", $PHPSPLOIT['FILE']);
}

// r['stat']
@clearstatcache();
if (!($r = @lstat($path)))
    return error("%s: Permission denied", $PHPSPLOIT['FILE']);

$r["file_repr"] = $file_repr;

$r["atime"] = date("Y-m-d H:i:s O", $r["atime"]);
$r["mtime"] = date("Y-m-d H:i:s O", $r["mtime"]);
$r["ctime"] = date("Y-m-d H:i:s O", $r["ctime"]);

if (extension_loaded("posix"))
{
    $r["posix_pwuid"] = posix_getpwuid($r["uid"])["name"];
    $r["posix_grgid"] = posix_getgrgid($r["gid"])["name"];
}

return $r;

?>
