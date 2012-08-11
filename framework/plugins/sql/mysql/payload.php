<?php

$connect = @mysql_connect($Q['HOST'],$Q['USER'],$Q['PASS']);
if (!$connect) return error('ERROR '.mysql_errno().': '.mysql_error());

if (@$Q['BASE']){
    $select = @mysql_select_db($Q['BASE'],$connect);
    if (!$select) return error('ERROR '.mysql_errno().': '.mysql_error());}

$query = mysql_query($Q['QUERY'],$connect);
if (!$query) return error('ERROR '.mysql_errno().': '.mysql_error());

$rows = @mysql_num_rows($query);
$result = False;
if (is_int($rows)){
    if ($rows>0){
        $result = array();
        $x = mysql_fetch_array($query, MYSQL_ASSOC);
        $result[] = array_keys($x);
        $result[] = array_values($x);
        while ($line = mysql_fetch_array($query, MYSQL_ASSOC)){
            $result[] = array_values($line);}

    return array('get',$rows, $result);}}

$rows = @mysql_affected_rows();
if (is_int($rows)) return array('set',$rows);

return error('ERROR '.mysql_errno().': '.mysql_error());

?>
