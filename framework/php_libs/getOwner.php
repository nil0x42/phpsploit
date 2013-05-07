<?

function getOwner($absFilePath){
    $uid = @filegroup($absFilePath);
    $result = '?';
    if (function_exists('posix_getpwuid')){
        $usr = @posix_getpwuid($uid);
        if (isset($usr['name'])){
            if (is_string($usr['name'])){
                if ($usr['name']){
                    $result = $usr['name'];}}}}
    return($result);}

?>
