<?php

!import(getOwner)
!import(getGroup)
!import(getMTime)
!import(getPerms)
!import(getSize)
!import(dirAccess)
!import(fileAccess)


$file = $Q['TARGET'];
$r = array();

$wmode = getPerms($file,'win');
$owner = getOwner($file);
$group = getGroup($file);


$r['mode'] = $wmode;
$x = $owner.$group;
if ($x != '??'){
    $r['mode'] = getPerms($file);
    $r['owner'] = $owner;
    $r['group'] = $group;}


$r['size']  = getSize($file);
$r['mtime'] = getMTime($file,'D M d H:i:s O Y');

$r['type']  = $wmode[0];

$r['write'] = ($wmode[1]!=='-') ? 'Yes' : 'No';
$r['read']  = ($wmode[2]!=='-') ? 'Yes' : 'No';
$r['exec']  = ($wmode[3]!=='-') ? 'Yes' : 'No';

if ($r['mode'][0]=='d'){
    $r['read']  = (dirAccess($file,'r')) ? 'Yes' : 'No';
    $r['write'] = (dirAccess($file,'w')) ? 'Yes' : 'No';}

if ($r['mode'][0]=='-'){
    $r['read']  = (fileAccess($file,'r')) ? 'Yes' : 'No';
    $r['write'] = (fileAccess($file,'w')) ? 'Yes' : 'No';}

return($r);
?>
