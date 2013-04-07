<?

!import(dirAccess)

if (@file_exists($Q['DIR'])){
    if ((@fileperms($Q['DIR']) & 0x4000) == 0x4000){
        if (@rmdir($Q['DIR'])) return 'ok';
        else{
            if (dirAccess($Q['DIR'],'r')) return error('notempty');
            else return error('noright');}}
    else return error('notadir');}
else return error('noexists');

?>
