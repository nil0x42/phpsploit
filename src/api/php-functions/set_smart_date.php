<?

// set_smart_date($smart_date) (type => string):
//      Return an unix timestamp from a value returned by
//      phpsploit's python get_smart_date() function.
//
//      >>> # if a date string is given, return timestamp
//      >>> set_smart_date("2011-09-11 13:29:42")
//      1315747782
//  NOTE: if string is empty or NULL, function returns current time

function set_smart_date($smart_date)
{
    if ($smart_date)
        return strtotime($smart_date);
    return time();
}

?>
