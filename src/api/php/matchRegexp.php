<?

function matchRegexp($name,$regexp){
    if ($regexp == '') return(TRUE);
    elseif (strstr($regexp,'*') === FALSE){
        if ($name == $regexp) return(TRUE);
        else return(FALSE);}
    else {
        $name = str_replace('.','\.',$name);
        $match = '(^'.str_replace('*','.*',$regexp).'$)';
        if (preg_match($match,$name)) return(TRUE);
        else return(FALSE);}}

?>
