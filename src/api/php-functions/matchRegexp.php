<?

// matchRegexp($name, $regexp) (type => boolean):
//      This function has a behavior similar to glob(3).
//      It checks if the given $name matches $regexp.
//
//      $name (string):
//          A common string (may be a filename for some use cases).
//
//      $regexp (string):
//          The pattern used to compare the regex.
//
//  EXAMPLE:
//      >>> matchRegexp("data.txt", "*.txt")
//      True
//      >>> matchRegexp("data.txt", "[A-Z]*")
//      False
//      >>> matchRegexp("Data.txt", "[A-Z]*")
//      True

function matchRegexp($name, $regexp)
{
    if ($regexp == '')
        return (True);
    elseif (strstr($regexp, '*') === False)
    {
        if ($name == $regexp)
            return (True);
        else
            return (False);
    }
    else
    {
        $name = str_replace('.', '\.', $name);
        $match = '(^' . str_replace('*', '.*', $regexp) . '$)';
        if (preg_match($match, $name))
            return (True);
        else
            return (False);
    }
}

?>
