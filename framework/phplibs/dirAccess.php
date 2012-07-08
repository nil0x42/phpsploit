<?

function dirAccess($absDirPath,$mode){
    global $Q;
    if ($mode == 'r'){
        if ($h = @opendir($absDirPath)){
            closedir($h);
            return(True);}
        else return(False);}
    elseif ($mode == 'w'){
        $rand = $absDirPath.uniqid('/pspapi_');
        if ($h = @fopen($rand,'a')){
            fclose($h);
            unlink($rand);
            return(True);}
        else return(False);}
    else return(False);}

?>
