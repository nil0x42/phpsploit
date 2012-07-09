<?

function getGroup($absFilePath){
    $gid = @filegroup($absFilePath);
    $result = '?';
    if (function_exists('posix_getgrgid')){
        $grp = @posix_getgrgid($gid);
        if (isset($grp['name'])){
            if (is_string($grp['name'])){
                if ($grp['name']){
                    $result = $grp['name'];}}}}
    return($result);}

?>
