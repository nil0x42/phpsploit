<?

!import(fileAccess)
!import(dirAccess)

function getPerms($absFilePath,$permstype='nix'){
    global $Q;
    $perms = @fileperms($absFilePath);
    if     (($perms & 0xC000) == 0xC000) {$type = 's';} // socket
    elseif (($perms & 0xA000) == 0xA000) {$type = 'l';} // symlink
    elseif (($perms & 0x8000) == 0x8000) {$type = '-';} // file
    elseif (($perms & 0x6000) == 0x6000) {$type = 'b';} // special block
    elseif (($perms & 0x4000) == 0x4000) {$type = 'd';} // dir
    elseif (($perms & 0x2000) == 0x2000) {$type = 'c';} // special char
    elseif (($perms & 0x1000) == 0x1000) {$type = 'p';} // fifo pipe
    else {                                $type = 'u';} // unknow
    if ((substr($absFilePath,-3) == $Q['SEPARATOR'].'..') || (substr($absFilePath,-2) == $Q['SEPARATOR'].'.')){
        $type = 'd';}

    if ($permstype == 'nix'){
        // Autres
        $info = "";
        $info .= (($perms & 0x0100) ? 'r' : '-');
        $info .= (($perms & 0x0080) ? 'w' : '-');
        $info .= (($perms & 0x0040) ?
                    (($perms & 0x0800) ? 's' : 'x' ) :
                    (($perms & 0x0800) ? 'S' : '-'));
        // Groupe
        $info .= (($perms & 0x0020) ? 'r' : '-');
        $info .= (($perms & 0x0010) ? 'w' : '-');
        $info .= (($perms & 0x0008) ?
                    (($perms & 0x0400) ? 's' : 'x' ) :
                    (($perms & 0x0400) ? 'S' : '-'));
        // Tout le monde
        $info .= (($perms & 0x0004) ? 'r' : '-');
        $info .= (($perms & 0x0002) ? 'w' : '-');
        $info .= (($perms & 0x0001) ?
                    (($perms & 0x0200) ? 't' : 'x' ) :
                    (($perms & 0x0200) ? 'T' : '-'));}

    else{
        $Rperm = (($perms & 0x0004) ? 'r' : '-');
        $Wperm = (($perms & 0x0002) ? 'w' : '-');
        $Xperm = (($perms & 0x0001) ?
                    (($perms & 0x0200) ? 't' : 'x' ) :
                    (($perms & 0x0200) ? 'T' : '-'));

        if ($type == '-'){
            if (fileAccess($absFilePath,'r'))
                $Rperm = 'r';
            else
                $Rperm = '-';

            if (fileAccess($absFilePath,'w'))
                $Wperm = 'w';
            else
                $Wperm = '-';
            }

        if ($type == 'd'){
            if (dirAccess($absFilePath,'r'))
                $Rperm = 'r';
            else
                $Rperm = '-';}

        $info = $Rperm.$Wperm.$Xperm;

        }
    $result = $type.$info;
    return($result);}
?>
