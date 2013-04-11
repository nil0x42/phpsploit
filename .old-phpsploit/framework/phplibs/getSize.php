<?

function getSize($absFilePath){
    $size = @filesize($absFilePath);
    $units = array('','K','M','G','T');
    for ($i=0;$size>=1024 && $i<4;$i++) $size/=1024;
    $result = str_replace('.',',',round($size,1)).$units[$i];
    return($result);}

?>
