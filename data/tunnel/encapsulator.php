<?php

ini_set('display_errors', '1');
ini_set('error_reporting', E_ALL ^ E_NOTICE);

$PHPSPLOIT = array();

function error($a='', $b=False, $c=False, $d=False, $e=False)
{
    return (array('__ERROR__' => sprintf($a, $b, $c, $d, $e)));
}

function payload()
{
    %%PAYLOAD%%
}

$result = payload();

if (@array_keys($result) !== array('__ERROR__'))
    $result = array('__RESULT__' => $result);

echo gzcompress(serialize($result));

?>
