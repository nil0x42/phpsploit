<?

if (@file_exists($Q['FILE'])){
    if ((@fileperms($Q['FILE']) & 0x8000) == 0x8000){
        if (@unlink($Q['FILE'])) return 'ok';
        else return error('noright');}
    else return error('notafile');}
else return error('noexists');

?>
