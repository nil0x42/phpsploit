<?php

// Disable SSL verification
putenv('LDAPTLS_REQCERT=never');

if(!$ldapConnexion = ldap_connect($PHPSPLOIT['HOST'])) {
   return error("Socket connexion failed ");
}
ldap_set_option($ldapConnexion, LDAP_OPT_PROTOCOL_VERSION, $PHPSPLOIT['VERSION']);

// Authentication or anonymous
if($PHPSPLOIT['LOGIN'] != " " and $PHPSPLOIT['PASS'] != " ") {
    $isAuth = ldap_bind($ldapConnexion, $PHPSPLOIT['LOGIN'], $PHPSPLOIT['PASS']);
} else {
    $isAuth = ldap_bind($ldapConnexion);
}

if(!$isAuth) {
    if (ldap_get_option($ldapConnexion, LDAP_OPT_DIAGNOSTIC_MESSAGE, $extended_error)) {
        return error("Error: Autentication failed %s", $extended_error);
    } else {
        return error("Autentication failed  ");
    }
}

$result = ldap_list($ldapConnexion, $PHPSPLOIT['BASE_DN'], "(objectClass=*)");
$datas  = ldap_get_entries($ldapConnexion, $result);

ldap_close($ldapConnexion);

if(!$datas) {
    return error('Something went wrong. Check your credentials.');
}

// Fix for printing
function clearNode(&$node) {
    foreach($node as $key => &$val) {
        if(!is_array($val)) {
            if(!ctype_print($val)) {
                $val = base64_encode($val);
            }
        } else {
            clearNode($val);
        }
    }
}

clearNode($datas);

return $datas;
?>