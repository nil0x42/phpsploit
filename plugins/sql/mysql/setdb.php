<?php

// Establish connection
$host = $PHPSPLOIT["HOST"];
$user = $PHPSPLOIT["USER"];
$pass = $PHPSPLOIT["PASS"];
$conn = @mysql_connect($host, $user, $pass);
if (!$conn)
    return error("ERROR: %s: %s", @mysql_errno(), @mysql_error());


// Select database
$base = $PHPSPLOIT["BASE"];
$select = @mysql_select_db($base, $conn);
if (!$select)
    return error("ERROR: %s: %s", @mysql_errno(), @mysql_error());

//@mysql_close($connect);
// NOTE:
// commented due to a bug in rare servers (bug found in iis6.0/php5.2.11)

return "OK";

?>
