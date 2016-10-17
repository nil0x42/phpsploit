<?php

!import(set_smart_date);

$target = $PHPSPLOIT['FILE'];
$ref = $PHPSPLOIT['REF'];

if ($ref !== NULL)
{
    if (($timestamp = @filemtime($ref)) === FALSE)
        return error("cannot stat '%s': No such file or directory", $ref);
}
else
    $timestamp = set_smart_date($PHPSPLOIT['TIME']);

if (@touch($target, $timestamp))
    return 'OK';

if (@file_exists($target))
    return error("%s: Permission denied", $target);

return error("%s: No such file or directory", $target);

?>
