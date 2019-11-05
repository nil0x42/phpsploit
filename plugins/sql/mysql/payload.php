<?php

!import(mysqli_compat)

// Establish connection
$host = $PHPSPLOIT["HOST"];
$user = $PHPSPLOIT["USER"];
$pass = $PHPSPLOIT["PASS"];
$conn = @mysqli_connect($host, $user, $pass);
if (!$conn)
    return error("ERROR: %s: %s", @mysqli_connect_errno(), @mysqli_connect_error());


// Select database (if any)
if (isset($PHPSPLOIT["BASE"]))
{
    $select = @mysqli_select_db($conn, $PHPSPLOIT['BASE']);
    if (!$select)
        return error("ERROR: %s: %s", @mysqli_errno($conn), @mysqli_error($conn));
}


// Send query
$query = mysqli_query($conn, $PHPSPLOIT['QUERY']);
if (!$query)
    return error("ERROR: %s: %s", @mysqli_errno($conn), @mysqli_error($conn));


// Query type: GET (information gathering)
$rows = @mysqli_num_rows($query);
if (is_int($rows))
{
    $result = array();
    $obj = mysqli_fetch_array($query, MYSQLI_ASSOC);
    $result[] = array_keys($obj);
    $result[] = array_values($obj);
    while ($line = mysqli_fetch_array($query, MYSQLI_ASSOC))
        $result[] = array_values($line);
    return array('GET', $rows, $result);
}


// Query type: SET (write into the database)
$rows = @mysqli_affected_rows($conn);
if (is_int($rows))
    return array('SET', $rows);

return error("ERROR: %s: %s", @mysqli_errno($conn), @mysqli_error($conn));

?>
