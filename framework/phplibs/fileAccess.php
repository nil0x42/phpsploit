<?

function fileAccess($absFilePath,$mode){
    if ($mode != 'r') $mode = 'a';
    if ($h = @fopen($absFilePath,$mode)){
        fclose($h);
        return(True);}
    else return(False);}

?>
