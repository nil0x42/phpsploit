<?

!import(getPerms)

if (getPerms($PHPSPLOIT['BACKDOOR']) != '-rwsrwxrwx')
    return error("%s: Is not a valid backdoor", $PHPSPLOIT['BACKDOOR']);

?>
