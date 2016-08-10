<?php


$ip = $PHPSPLOIT['IP'];
$ports = array();
for($i = $PHPSPLOIT['PORT_MIN']; $i <= $PHPSPLOIT['PORT_MAX']; $i++) {
    if(@fsockopen( $ip, $i, $errstr, $errno, floatval($PHPSPLOIT['TIMEOUT']) )) {
        $ports []= $i;
    }
}

return $ports;

?>