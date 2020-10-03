<?php
if (strtoupper(substr(PHP_OS, 0, 3)) === 'WIN') {
	$results = win32_ps_list_procs()
} else {
	$results = system("ps -a");
}
return $results;
?>