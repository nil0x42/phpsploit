<?php

!import(getOwner)
!import(getGroup)
!import(getMTime)
!import(getPerms)
!import(getSize)
!import(dirAccess)
!import(fileAccess)
!import(matchRegexp)

function printLst($lsdir, $regex)
{
    $text = array();
    if ($dh = @opendir($lsdir))
    {
        while (($elem = readdir($dh)) !== FALSE)
        {
            if (matchRegexp($elem,$regex))
            {
                $elempath = $lsdir.$elem;
                $mode  = getPerms($elempath);
                $wmode = getPerms($elempath, 'win');
                $owner = getOwner($elempath);
                $group = getGroup($elempath);
                $size  = getSize($elempath);
                $time  = getMTime($elempath, 'D M d H:i:s O Y');
                $text[] = array($mode, $wmode, $owner, $group, $size, $time, $elem);
            }
        }
        closedir($dh);
    }
    return ($text);
}

$lsdir = $PHPSPLOIT['TARGET'] . $PHPSPLOIT['SEPARATOR'];
$regex = '';
$ERROR = '';

if (!dirAccess($lsdir,'r'))
{
    if (@is_dir($lsdir))
        $ERROR = error("cannot open %s: Permission denied", substr($lsdir,0,-1));
    elseif ($PHPSPLOIT['PARSE'])
    {
        $split = strrpos($PHPSPLOIT['TARGET'], $PHPSPLOIT['SEPARATOR']) + 1;
        $lsdir = substr($PHPSPLOIT['TARGET'], 0, $split);
        $regex = substr($PHPSPLOIT['TARGET'], $split);
    }
}

if (strstr(substr($lsdir, 0, -1), $PHPSPLOIT['SEPARATOR']) === FALSE)
    $dirname = $lsdir;
else
    $dirname = substr($lsdir, 0, -1);

if (dirAccess($lsdir, 'r'))
{
    $R = array($dirname, $regex, printLst($lsdir, $regex));
    if (!count($R[2]))
        return error("%s: no elements matching '%s'", $dirname, $regex);
    else
        return $R;
}

elseif (!$ERROR)
{
    if (@is_dir($lsdir))
        return error("cannot open %s: Permission denied", $dirname);
    else
        return error("cannot access %s: No such file or directory.", $dirname);
}

else
    return $ERROR;

?>
