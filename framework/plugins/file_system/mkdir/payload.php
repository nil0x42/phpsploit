<?

if (!@file_exists($Q['DIR'])){
    if (@mkdir($Q['DIR'])) return 'ok';
    else{
        $dirname = substr($Q['DIR'],0,strrpos($Q['DIR'],$Q['SEPARATOR'])+1);
        if (@file_exists($dirname)) return error('noright',$Q['DIR']);
        else return error('noexists',$Q['DIR']);}}
else return error('exists',$Q['DIR']);

?>
