<?

function getMTime($absFilePath,$dateFormat){
    $mtime  = @filemtime($absFilePath);
    $result = @date($dateFormat,$mtime);
    return($result);}

?>
