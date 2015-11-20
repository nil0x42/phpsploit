<?php

if (!function_exists("oci_connect"))
    return error("ERROR: PECL OCI8 >= 1.1.0 required");

// Establish connection
function oracle_login($info, $connector, $serv_type)
{
    $conn_str = '( DESCRIPTION =
                    ( ADDRESS =
                        ( PROTOCOL = TCP )
                        ( HOST = ' . $info["HOST"] . ')
                        ( PORT = ' . $info["PORT"] . ') )
                    ( CONNECT_DATA =
                        ( ' . $connector . ' = ' . $info["CONNECTOR"] . ')
                        ( SERVER = ' . $serv_type . ') ) )';
    $c = @ocilogon($info["USER"], $info["PASS"], $conn_str);
    return ($c);
}

$conn = False;
if ($conn === False)
    $conn = oracle_login($PHPSPLOIT, "SERVICE_NAME", "POOLED");
if ($conn === False)
    $conn = oracle_login($PHPSPLOIT, "SERVICE_NAME", "DEDICATED");
if ($conn === False)
    $conn = oracle_login($PHPSPLOIT, "SID", "POOLED");
if ($conn === False)
    $conn = oracle_login($PHPSPLOIT, "SID", "DEDICATED");

if ($conn === False)
{
    $err = @oci_error();
    return error("ERROR: %s: %s", $err["code"], $err["message"]);
}

return "OK";

?>
