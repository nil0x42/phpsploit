<?php

function phpinfo_html()
{
    ob_start();
    phpinfo(-1);
    $pi = ob_get_clean();

    return $pi;
}

return phpinfo_html();

?>
