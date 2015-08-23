<?php

// Establish connection
$host = $PHPSPLOIT["HOST"];
$user = $PHPSPLOIT["USER"];
$pass = $PHPSPLOIT["PASS"];
$conn = @mysql_connect($host, $user, $pass);
if (!$conn)
    return error("ERROR: %s: %s", @mysql_errno(), @mysql_error());


// Select database (if any)
if (isset($PHPSPLOIT["BASE"]))
{
    $select = @mysql_select_db($PHPSPLOIT['BASE'], $conn);
    if (!$select)
        return error("ERROR: %s: %s", @mysql_errno(), @mysql_error());
}


// Send query
$query = mysql_query($PHPSPLOIT['QUERY'], $conn);
if (!$query)
    return error("ERROR: %s: %s", @mysql_errno(), @mysql_error());


// Query type: GET (information gathering)
$rows = @mysql_num_rows($query);
if (is_int($rows))
{
    $result = array();
    $obj = mysql_fetch_array($query, MYSQL_ASSOC);
    $result[] = array_keys($obj);
    $result[] = array_values($obj);
    while ($line = mysql_fetch_array($query, MYSQL_ASSOC))
        $result[] = array_values($line);
    return array('GET', $rows, $result);
}


// Query type: SET (write into the database)
$rows = @mysql_affected_rows();
if (is_int($rows))
    return array('SET', $rows);

return error("ERROR: %s: %s", @mysql_errno(), @mysql_error());

?>
