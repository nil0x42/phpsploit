<?php

!import(mysqli_compat)

// Establish connection
$host = $PHPSPLOIT["HOST"];
$user = $PHPSPLOIT["USER"];
$pass = $PHPSPLOIT["PASS"];

$conn = @mysqli_connect($host, $user, $pass);
if (!$conn)
    return error("ERROR: %s: %s", @mysqli_connect_errno(), @mysqli_connect_error());

//@mysql_close($connect);
// NOTE:
// commented due to a bug in rare servers (bug found in iis6.0/php5.2.11)

return "OK";

?>
