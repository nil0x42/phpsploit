<?php

!import(getSize)
!import(dirAccess)
!import(getPerms)
!import(matchRegexp)

function dir_scan($path){
    global $Q, $R;
    if ($h = @opendir($path)){
        while (($elem = readdir($h)) !== FALSE){
            if ($elem != '.' && $elem != '..'){
                if ((@fileperms($path.$elem) & 0x4000) == 0x4000){
                    dir_scan($path.$elem.$Q['SEPARATOR']);}
                elseif (matchRegexp($elem,$Q['PATTERN'])){
                    $relPath = $path;
                    $R[] = array(getPerms($path.$elem,'win'),getSize($path.$elem),$relPath.$elem);}}}
        closedir($h);}}

if (dirAccess($Q['DIR'],'r')) dir_scan($Q['DIR'].$Q['SEPARATOR']);
else{
    if (@file_exists($Q['DIR'])){
        if ((@fileperms($Q['DIR']) & 0x4000) == 0x4000) return error('noright');
        else return error('notadir');}
    else return error('noexists');}

if (!$R) return error('nomatch');

return $R;


?>
