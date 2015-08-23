<?php

if (!function_exists("oci_connect"))
    return error("ERROR: PECL OCI8 >= 1.1.0 required");

// Establish connection
function oracle_login($info, $serv_type)
{
    $conn_str = '( DESCRIPTION =
                    ( ADDRESS =
                        ( PROTOCOL = TCP )
                        ( HOST = ' . $info["HOST"] . ')
                        ( PORT = ' . $info["PORT"] . ') )
                    ( CONNECT_DATA =
                        ( SERVICE_NAME = ' . $info["BASE"] . ')
                        ( SERVER = ' . $serv_type . ') ) )';
    $c = @ocilogon($info["USER"], $info["PASS"], $conn_str);
    return ($c);
}

$conn = oracle_login($PHPSPLOIT, "POOLED");
if (!$conn)
    $conn = oracle_login($PHPSPLOIT, "DEDICATED");

if (!$conn)
{
    $err = @oci_error();
    return error("ERROR: %s: %s", $err["code"], $err["message"]);
}

// Send query
$query = @ociparse($conn, $PHPSPLOIT['QUERY']);
if (!$query)
{
    $err = @oci_error();
    return error("ERROR: %s: %s", $err["code"], $err["message"]);
}
$statement_type = @ocistatementtype($query);

if (!ociexecute($query))
{
    $err = @oci_error($query);
    return error("ERROR: %s: %s", $err["code"], $err["message"]);
}

if ($statement_type == "SELECT")
{
    $result = array();
    $obj = oci_fetch_array($query, OCI_ASSOC+OCI_RETURN_NULLS);
    $result[] = array_keys($obj);
    $result[] = array_values($obj);
    while ($line = oci_fetch_array($query, OCI_ASSOC+OCI_RETURN_NULLS))
        $result[] = array_values($line);
    return array('GET', count($result) - 1, $result);
}
else
{
    $rows = @ocirowcount($query);
    return array('SET', $rows);
}

?>
