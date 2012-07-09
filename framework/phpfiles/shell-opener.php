<?

!import(execute);
!import(dirAccess);

function getTmpDir(){
    if(!function_exists('sys_get_temp_dir')){
        if(!empty($_ENV['TMP']))$t=$_ENV['TMP'];
        elseif(!empty($_ENV['TMPDIR']))$t=$_ENV['TMPDIR'];
        elseif(!empty($_ENV['TEMP']))$t=$_ENV['TEMP'];
        else{
            $t=tempnam(":\n\\/?><","dkdk");
            if(@file_exists($t))@unlink($t);
            $t=dirname($t);}}
    else $t=sys_get_temp_dir();
    return(realpath($t));}


$R = $_SERVER;

$R['PHP_OS']      = PHP_OS;
$R['PHP_VERSION'] = PHP_VERSION;
$R['WHOAMI']      = @execute('whoami');

$tmp = @execute('echo $HOME');
$R['HOME'] = ($tmp!='$HOME' && $tmp) ? $tmp : '';


// GET THE WEB ROOT
$R['WEBROOT'] = $R['DOCUMENT_ROOT'];
if(!$R['WEBROOT']){
    $R['WEBROOT']=$R['APPL_PHYSICAL_PATH'];}
if(!$R['WEBROOT']){
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
                $R['WEBROOT']=substr($abs,0,-$len);}}}}
$R['WEBROOT'] = realpath($R['WEBROOT']);


// GET A WRITABLE DIR FROM WEB PATH
$MAX_RECURSION=6;
$DIRS=Array($R['WEBROOT']);
$R['W_WEBDIR']='';
for ($recLvl=1;$recLvl<=$MAX_RECURSION;$recLvl++){
    foreach($DIRS as $dir){
        if (dirAccess($dir,'w')){
            $R['W_WEBDIR'] = realpath($dir);
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
$R['W_TMPDIR'] = (dirAccess($tmp,'w')) ? $tmp : $R['W_WEBDIR'];


return $R;


?>
