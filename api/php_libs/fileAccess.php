<?

// this function checks the given access code (r or w)
// and returns a boolean value.

function fileAccess($absFilePath, $mode) {
    // convert 'w' mode into 'a', because we don't want to
    // empty the file by testing !
    if ($mode != 'r')
        $mode = 'a';

    // fopen() the given file path and return Ture in case of success
    if ($h = @fopen($absFilePath, $mode)){
        fclose($h);
        return(True);
        }
    else
        return(False);
    }

?>
