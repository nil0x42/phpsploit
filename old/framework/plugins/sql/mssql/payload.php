<?php

$connect = @mssql_connect($Q['HOST'],$Q['USER'],$Q['PASS']);
if (!$connect) return error('ERROR '.mssql_errno().': '.mssql_error());

if (@$Q['BASE']){
    $select = @mssql_select_db($Q['BASE'],$connect);
    if (!$select) return error('ERROR '.mssql_errno().': '.mssql_error());}

$query = mssql_query($Q['QUERY'],$connect);
if (!$query) return error('ERROR '.mssql_errno().': '.mssql_error());

$rows = @mssql_num_rows($query);
$result = False;
if (is_int($rows)){
    if ($rows>0){
        $result = array();
        $x = mssql_fetch_array($query, MSSQL_ASSOC);
        $result[] = array_keys($x);
        $result[] = array_values($x);
        while ($line = mssql_fetch_array($query, MSSQL_ASSOC)){
            $result[] = array_values($line);}

    return array('get',$rows, $result);}}

$rows = @mssql_rows_affected();
if (is_int($rows)) return array('set',$rows);

return error('ERROR '.mssql_errno().': '.mssql_error());

?>
