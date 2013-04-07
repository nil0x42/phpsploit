<?php

$connect = @mysql_connect($Q['HOST'],$Q['USER'],$Q['PASS']);
if (!$connect) return error('ERROR '.@mysql_errno().': '.@mysql_error());

//@mysql_close($connect); // commented due to a bug in rare servers (bug found in iis6.0/php5.2.11

return 'ok';

?>
