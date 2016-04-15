<?php

!import(set_smart_date);

$target = $PHPSPLOIT['FILE'];
$timestamp = set_smart_date($PHPSPLOIT['TIME']);

if (@touch($target, $timestamp))
    return 'OK';

if (@file_exists($target))
    return error("%s: Permission denied", $target);

return error("%s: No such file or directory", $target);

?>
