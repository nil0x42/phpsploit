<?

// getSize($abspath) (type => string):
//      Returns the size of the given file path in human format.
//
//      $abspath (string):
//          This variable should be an existing absolute file path
//
//  EXAMPLE:
//      >>> getSize("/etc/passwd")
//      "1.4K"

function getSize($abspath)
{
    $size = @filesize($abspath);
    $units = array('', 'K', 'M', 'G', 'T');

    for ($i = 0; $size >= 1024 && $i < 4; $i++)
        $size /= 1024;
    $result = str_replace('.', ',', round($size, 1)) . $units[$i];
    return ($result);
}

?>
