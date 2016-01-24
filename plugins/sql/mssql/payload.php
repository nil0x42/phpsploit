<?php

// Establish connection
$host = $PHPSPLOIT["HOST"];
$user = $PHPSPLOIT["USER"];
$pass = $PHPSPLOIT["PASS"];
$conn = @mssql_connect($host, $user, $pass);
if (!$conn)
    return error("ERROR: %s", @mssql_get_last_message());


// Select database (if any)
if (isset($PHPSPLOIT["BASE"]))
{
    $select = @mssql_select_db($PHPSPLOIT['BASE'], $conn);
    if (!$select)
        return error("ERROR: %s", @mssql_get_last_message());
}


// Send query
$query = mssql_query($PHPSPLOIT['QUERY'], $conn);
if (!$query)
    return error("ERROR: %s", @mssql_get_last_message());


// Query type: GET (information gathering)
$rows = @mssql_num_rows($query);
if (is_int($rows))
{
    $result = array();
    $obj = mssql_fetch_array($query, MSSQL_ASSOC);
    $result[] = array_keys($obj);
    $result[] = array_values($obj);
    while ($line = mssql_fetch_array($query, MSSQL_ASSOC))
        $result[] = array_values($line);
    return array('GET', $rows, $result);
}


// Query type: SET (write into the database)
$rows = @mssql_rows_affected();
if (is_int($rows))
    return array('SET', $rows);

return error("ERROR: %s", @mssql_get_last_message());

?>
