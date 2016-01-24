<?php

// Establish connection
$host = $PHPSPLOIT["HOST"];
$user = $PHPSPLOIT["USER"];
$pass = $PHPSPLOIT["PASS"];
$conn = @mssql_connect($host, $user, $pass);
if (!$conn)
    return error("ERROR: %s", @mssql_get_last_message());

//@mssql_close($connect);
// NOTE:
// commented due to a bug in rare servers (bug found in iis6.0/php5.2.11)

return "OK";

?>
