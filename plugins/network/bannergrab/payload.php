<?php
$addr = $PHPSPLOIT['IP'];

$timeout = $PHPSPLOIT['TIMEOUT'];

$ports = range($PHPSPLOIT['PORT_MIN'], $PHPSPLOIT['PORT_MAX']);
shuffle($ports);

$results = array();
foreach ($ports as $port) {
	$sock = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
	socket_set_option($sock, SOL_SOCKET, SO_RCVTIMEO, array('sec'=>$timeout, 'usec'=>0));
	socket_set_option($sock, SOL_SOCKET, SO_SNDTIMEO, array('sec'=>$timeout, 'usec'=>0));
	if (@socket_connect($sock, $IP, $port)) {
		socket_recv($sock, $buffer, 1024, 0);
		$results[] = array($port, "OPEN", $buffer);
	} else {
		$results[] = array($port, "CLOSED", "");
	}
    socket_close($sock);
}
print_r(json_encode($results));
return $result;
?>
