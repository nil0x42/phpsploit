<?

// getMTime($abspath, $date_fmt) (type => string):
//      Return $abspath file last modification time (mtime)
//      in $data_fmt format (the format used by the php date() function).
//
//      $abspath (string):
//          This variable should be an existing absolute file path
//
//      $date_fmt (string):
//          A string representing a date format. For more infos, take
//          a look at: http://www.php.net/manual/en/function.date.php

function getMTime($abspath, $date_fmt)
{
    $mtime = @filemtime($abspath);
    $result = @date($date_fmt, $mtime);
    return ($result);
}

?>
