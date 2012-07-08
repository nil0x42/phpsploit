<?php

!import(getOwner)
!import(getGroup)
!import(getMTime)
!import(getPerms)
!import(getSize)
!import(dirAccess)
!import(fileAccess)
!import(matchRegexp)

function printLst($lsdir,$regex){
    $text = array();
    if ($dh = @opendir($lsdir)){
        while (($elem = readdir($dh)) !== FALSE){
            if (matchRegexp($elem,$regex)){
                $elempath = $lsdir.$elem;
                $mode  = getPerms($elempath);
                $wmode = getPerms($elempath,'win');
                $owner = getOwner($elempath);
                $group = getGroup($elempath);
                $size  = getSize($elempath);
                $time  = getMTime($elempath,'D M d H:i:s O Y');
                $text[] = array($mode,$wmode,$owner,$group,$size,$time,$elem);}}
        closedir($dh);}
    return($text);}

$lsdir = $Q['TARGET'].$Q['SEPARATOR'];
$regex = '';
$ERROR = '';

if (!dirAccess($lsdir,'r')){
    if (is_dir($lsdir)) $ERROR = error('noright',substr($lsdir,0,-1));
    elseif($Q['PARSE']){
        $lsdir = substr($Q['TARGET'],0,strrpos($Q['TARGET'],$Q['SEPARATOR'])+1);
        $regex = substr($Q['TARGET'],strrpos($Q['TARGET'],$Q['SEPARATOR'])+1);}}

$dirname = (strstr(substr($lsdir,0,-1),$Q['SEPARATOR']) === FALSE) ? $lsdir : substr($lsdir,0,-1);

if (dirAccess($lsdir,'r')){
    $R = array($dirname,$regex,printLst($lsdir,$regex));
    if (!count($R[2])) return error('nomatch', $dirname, $regex);
    else return $R;}

elseif (!$ERROR){
    if (is_dir($lsdir)) return error('noright',$dirname);
    else return error('nodir',$dirname);}

else return $ERROR;

?>
