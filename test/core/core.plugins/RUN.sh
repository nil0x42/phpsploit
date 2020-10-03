#!/bin/bash

n_plugs=`find $ROOTDIR/plugins/*/* -maxdepth 0 | wc -l`
n_plugs_plus2=$(( $n_plugs + 2 ))

###
### Test `core.plugins` package (plugin loader / launcher)
###

# before bugged plugins, check that all plugins are correctly loaded
$PHPSPLOIT -e exit > $TMPFILE
assert_contains $TMPFILE " $n_plugs plugins correctly loaded$"
assert_not_contains $TMPFILE "error.* encountered while loading plugins"
# reload-plugins should be ok, because there is no error
$PHPSPLOIT -e 'corectl reload-plugins' > /dev/null || FAIL



###
### Custom Setup (voluntary bugged USERDIR plugins)
###
cp -r "$PHPSPLOIT_CONFIG_DIR" "$TMPFILE-conf"
export PHPSPLOIT_CONFIG_DIR="$TMPFILE-conf"
rm -rf $TMPFILE-conf/plugins
cp -r $SCRIPTDIR/test-plugins $TMPFILE-conf/plugins
chmod 333 $TMPFILE-conf/plugins/valid_category-name/plugin-py_not-readable/plugin.py
sed -i "/VERBOSITY/d" $TMPFILE-conf/config


$PHPSPLOIT -e exit > $TMPFILE
assert_contains $TMPFILE << EOF
 $n_plugs_plus2 plugins correctly loaded$
^\[\#\] 5 errors encountered while loading plugins .*corectl reload-plugins
EOF
[ "$(wc -l < $TMPFILE)" -eq 2 ] || FAIL



###
### Check output of `help` after loading bugged plugins
###
$PHPSPLOIT -e 'exploit; help' > $TMPFILE
assert_not_contains $TMPFILE << EOF
invalid.category
  notloaded
  cannot-compile
  invalid-name.notloaded
  is-empty
  plugin-py_not-readable
EOF
assert_contains $TMPFILE << EOF
^Valid category-name Plugins$
  is-valid  
  is-in-existing_category  
EOF
# check this plugin is listed within default 'System Plugins' category
[ "$(grep -c "^System Plugins" $TMPFILE)" -eq 1 ] || FAIL
grep -A1 "is-in-existing_category" $TMPFILE | grep -q '  phpinfo  ' || FAIL



###
### Check output of `help` after loading bugged plugins
###

# reload-plugins should fail, because there is at least an error
$PHPSPLOIT -e 'corectl reload-plugins' > $TMPFILE && FAIL
sed -i -e "1,2d" $TMPFILE # remove 2 first lines (unwanted)

grep -A1 "^\[#\] Couldn't load category: '.*/plugins/invalid.category'$" $TMPFILE > $TMPFILE-out || FAIL
grep -q  "^\[#\]     Folder name doesn.*t match .*" $TMPFILE-out || FAIL

grep -A1 "^\[#\] Couldn't load plugin: '.*/plugins/valid_category-name/invalid-name.notloaded'$" $TMPFILE > $TMPFILE-out || FAIL
grep -q  "^\[#\]     Folder name doesn.*t match .*" $TMPFILE-out || FAIL

grep -A1 "^\[#\] Couldn't load plugin: '.*/plugins/valid_category-name/is-empty'$" $TMPFILE > $TMPFILE-out || FAIL
grep -q  "^\[#\]     File plugin.py is empty" $TMPFILE-out || FAIL

grep -A1 "^\[#\] Couldn't compile plugin: '.*/plugins/valid_category-name/cannot-compile'$" $TMPFILE > $TMPFILE-out || FAIL
grep -q  "^\[#\] Traceback (most recent call last):$" $TMPFILE-out || FAIL

grep -A1 "^\[#\] Couldn't load plugin: '.*/plugins/valid_category-name/plugin-py_not-readable'$" $TMPFILE > $TMPFILE-out || FAIL
grep -q  "^\[#\]     File error on plugin.py: " $TMPFILE-out || FAIL

assert_contains $TMPFILE << EOF
 $n_plugs_plus2 plugins correctly loaded$
^\[\#\] 5 errors encountered while loading plugins
EOF
assert_not_contains $TMPFILE "corectl reload-plugins"
