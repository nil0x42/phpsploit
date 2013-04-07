<?

$next = 1;
$path = substr($Q['ROOT'],0,-1);
foreach ($Q['ELEMS'] as $elem){
    if ($next){
        $path.=$Q['SEPARATOR'].$elem;
        if (!@mkdir($path)){
            if (!@file_exists($path)){
                return error('noright',$path);
                $next = 0;}}}}
return 'ok';

?>
