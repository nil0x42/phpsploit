<?

// mkdir recursively

$errmsg = "cannot create directory '%s': %s";

$path = $PHPSPLOIT['DRIVE'];
$err = NULL;

foreach ($PHPSPLOIT['PATH_ELEMS'] as $elem)
{
    $path .= $PHPSPLOIT['PATH_SEP'] . $elem;
    if (mkdir($path))
        $err = NULL;
    else
    {
        if (!file_exists($path))
            $err = error($errmsg, $path, "No such file or directory");
        elseif (!is_dir($path))
            $err = error($errmsg, $path, "Not a directory");
        else
            $err = error($errmsg, $path, "Permission denied");
    }
}
if ($err !== NULL)
    return $err;
else
    return 'OK';

?>
