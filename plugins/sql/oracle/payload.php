<?php

if (!function_exists("oci_connect"))
    return error("ERROR: PECL OCI8 >= 1.1.0 required");

// Establish connection (for deprecated ORACLE_CRED)
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

# DEFAULT CONNECT
if (isset($PHPSPLOIT['CONNSTR']))
{
    $user = $PHPSPLOIT["USER"];
    $pass = $PHPSPLOIT["PASS"];
    $connstr = $PHPSPLOIT["CONNSTR"];
    $charset = $PHPSPLOIT["CHARSET"];
    
    if ($charset)
        $conn = @ocilogon($user, $pass, $connstr, $charset);
    else
        $conn = @ocilogon($user, $pass, $connstr);
}
# DEPRECATED CONNECT
else
{
    $conn = False;
    if ($conn === False)
        $conn = oracle_login($PHPSPLOIT, "SERVICE_NAME", "POOLED");
    if ($conn === False)
        $conn = oracle_login($PHPSPLOIT, "SERVICE_NAME", "DEDICATED");
    if ($conn === False)
        $conn = oracle_login($PHPSPLOIT, "SID", "POOLED");
    if ($conn === False)
        $conn = oracle_login($PHPSPLOIT, "SID", "DEDICATED");
}

if ($conn === False)
{
    $err = @oci_error();
    return error("ERROR: ocilogon(): %s", $err["message"]);
}

// Send query
$query = @ociparse($conn, $PHPSPLOIT['QUERY']);
if (!$query)
{
    $err = @oci_error();
    return error("ERROR: ociparse(): %s", $err["message"]);
}
$statement_type = @ocistatementtype($query);

if (!ociexecute($query))
{
    $err = @oci_error($query);
    return error("ERROR: ociexecute(): %s", $err["message"]);
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
