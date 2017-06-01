<?php

if (!function_exists("oci_connect"))
    return error("ERROR: PECL OCI8 >= 1.1.0 required");

$user = $PHPSPLOIT["USER"];
$pass = $PHPSPLOIT["PASS"];
$connstr = $PHPSPLOIT["CONNSTR"];
$charset = $PHPSPLOIT["CHARSET"];

if ($charset)
    $conn = @ocilogon($user, $pass, $connstr, $charset);
else
    $conn = @ocilogon($user, $pass, $connstr);

if ($conn === False)
{
    $err = @oci_error();
    return error("ERROR: %s: %s", $err["code"], $err["message"]);
}

return "OK";

?>
