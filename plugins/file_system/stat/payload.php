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
    $tmp = posix_getpwuid($r["uid"]);
    $r["posix_pwuid"] = $tmp["name"];
    $tmp = posix_getgrgid($r["gid"]);
    $r["posix_grgid"] = $tmp["name"];
}

return $r;

?>
