<?php

if (@file_exists($Q['FILE'])){
    if ((@fileperms($Q['FILE']) & 0x8000) == 0x8000){
        if ($h = @fopen($Q['FILE'],'r')){
            $size = @filesize($Q['FILE']);
            if ($size == '0') return '';
            else {
                if ($data = fread($h,$size)){
                    return base64_encode($data);}
                else return error('noread');}
            fclose($h);}
        else return error('noread');}
    else return error('notafile');}
else return 'NEWFILE';

?>
