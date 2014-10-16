<?php

// backup current php config to restore it after payload execution
$orig_conf = ini_get_all();
foreach ($orig_conf as $key => $val)
{
    if ($val["access"] & 1)
        $orig_conf[$key] = $val["local_value"];
    else
        unset($orig_conf[$key]);
}

// be verbose on php errors
ini_set('display_errors', '1');
ini_set('error_reporting', E_ALL ^ E_NOTICE);

// container for dynamic input variables, transmitted from plugins
// at python side (plugin.py files).
$PHPSPLOIT = array();

// allows php-side plugins to use `return error("something")`
// with a printf()-like flavour.
// This is the correct way to inform the framework that output
// is an error message.
function error($a='', $b=False, $c=False, $d=False, $e=False)
{
    return (array('__ERROR__' => sprintf($a, $b, $c, $d, $e)));
}

// %%PAYLOAD%% is replaced by the dynamically built payload
// before each remote plugin execution.
function payload()
{
    %%PAYLOAD%%
}

// handle payload result and output it's gzipper content.
$result = payload();
if (@array_keys($result) !== array('__ERROR__'))
    $result = array('__RESULT__' => $result);
echo gzcompress(serialize($result));

// restore original php config, as they was pefore payload execution
foreach ($orig_conf as $key => $val)
    @ini_set($key, $val);

?>
