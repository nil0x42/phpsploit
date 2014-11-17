<?

// simple mkdir

$file = $PHPSPLOIT['DIR'];
$parent = dirname($file);
$errmsg = "cannot create directory '%s': %s";

if (file_exists($file))
    return error($errmsg, $file, "File exists");

if (mkdir($file))
    return 'OK';

if (!file_exists($parent))
    return error($errmsg, $file, "No such file or directory");

if (!is_dir($parent))
    return error($errmsg, $file, "Not a directory");

return error($errmsg, $file, "Permission denied");

?>
