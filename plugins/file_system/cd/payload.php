<?

!import(dirAccess)

if (dirAccess($Q['DIR'],'r')) return 'ok';
else{
    if (@file_exists($Q['DIR'])){
        if ((@fileperms($Q['DIR']) & 0x4000) == 0x4000) return error('noright');
        else return error('notadir');}
    else return error('noexists');}

?>
