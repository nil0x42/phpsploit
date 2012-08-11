<?

!import(fileAccess)

$source      = $Q['SOURCE'];
$destination = $Q['DESTINATION'];


if (@file_exists($source)){
    if ((@fileperms($source) & 0x8000) == 0x8000){
        if ($h = @fopen($source,'r')){
            $size = @filesize($source);
            if (!($data = fread($h,$size))) return error('src_noread');
            fclose($h);}
        else return error('src_noread',$source);}
    else return error('src_notafile',$source);}
else return error('src_noexists',$source);


if ((@fileperms($destination) & 0x4000) == 0x4000){
    $dirname     = (substr($destination,-1) == $Q['SEPARATOR']) ? $destination : $destination.$Q['SEPARATOR'];
    $destination = $dirname.basename($source);}

if (@file_exists($destination)){
    if ((@fileperms($destination) & 0x8000) == 0x8000){
        if (fileAccess($destination,'w')){
            if ($Q['FORCE']){
                if ($h = @fopen($destination,'w')){
                    @fwrite($h,$data);
                    @fclose($h);
                    return array('ok',$destination);}
                else return error('dst_nowrite',$destination);}
            else return error('dst_exists',$destination);}
        else return error('dst_nowrite',$destination);}
    else return error('dst_notafile',$destination);}
else{
    if ($h = @fopen($destination,'w')){
        @fwrite($h,$data);
        @fclose($h);
        return array('ok',$destination);}
    else{
        $dirname = substr($destination,0,strrpos($destination,$Q['SEPARATOR'])+1);
        if ((@fileperms($dirname) & 0x4000) == 0x4000) return error('dst_nowrite',$destination);
        else return error('dst_noexists',$destination);}}

?>
