<?

!import(getPerms)

if (getPerms($Q['BACKDOOR']) != '-rwsrwxrwx') return error('nok');
return 'ok';

?>
