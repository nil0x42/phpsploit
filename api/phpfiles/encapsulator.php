<?php

ini_set('display_errors','1');
ini_set('error_reporting',E_ALL^E_NOTICE);

$Q = array();
$R = array();

function error($name='', $arg1=False, $arg2=False, $arg3=False, $arg4=False)
{
    $args = array($name);

    if($arg1 !== False)
        $args[] = $arg1;
    if($arg2 !== False)
        $args[] = $arg2;
    if($arg3 !== False)
        $args[] = $arg3;
    if($arg4 !== False)
        $args[] = $arg4;

    return(array('__ERROR__' => $args));
}

function PAYLOAD()
{
    %%PAYLOAD%%
}

$RESULT = PAYLOAD();

if (@array_keys($RESULT) !== array('__ERROR__'))
    $RESULT = array('__RESULT__' => $RESULT);

echo gzcompress(serialize($RESULT));

?>
