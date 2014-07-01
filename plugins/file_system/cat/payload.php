<?php

if (@file_exists($ARG['FILE']))
{
    if ((@fileperms($ARG['FILE']) & 0x8000) == 0x8000)
    {
        if ($h = @fopen($ARG['FILE'], 'r'))
        {
            $size = @filesize($ARG['FILE']);
            if ($size == '0')
                return '';
            else
            {
                if ($data = fread($h, $size))
                    return base64_encode($data);
                else
                    return error("%s: Permission denied", $ARG['FILE']);
            }
            fclose($h);
        }
        else
            return error("%s: Permission denied", $ARG['FILE']);
    }
    else
        return error("%s: Not a file", $ARG['FILE']);
}
else
    return error("%s: No such file or directory", $ARG['FILE']);

?>
