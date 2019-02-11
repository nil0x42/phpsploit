#!/bin/bash

# Test `linebuf` module (linebuf.py)
# *LineBuffer classes are used as base class for
# phpsploit configuration settings.


###
### Test Setup
###

# set EDITOR to a custom script that copies buffer into $OUT file:
IN="$TMPFILE-EDITOR-IN"
OUT="$TMPFILE-EDITOR-OUT"
cat > $TMPFILE-EDITOR << EOF
#!/bin/bash
IN="$IN"
OUT="$OUT"
if [ -f "\$IN" ]; then
    cat "\$IN" > "\$1"
    rm -f "\$IN"
fi
cat "\$1" > "\$OUT"
EOF
chmod +x $TMPFILE-EDITOR
phpsploit_pipe set EDITOR "$TMPFILE-EDITOR" > /dev/null || FAIL

# $FILE_5LINES = readable file with 5 lines (and 3 valid lines)
FILE_5LINES=$TMPFILE-FILE_5LINES
cat > $FILE_5LINES << EOF
line1 %%PASSKEY%%
# comment (and then, emtpy line)

line4 %%PASSKEY%%
line5 %%PASSKEY%%
EOF

# $FILE_EMPTY = readable file with no content
FILE_EMPTY=$TMPFILE-FILE_EMPTY
> $FILE_EMPTY

# $FILE_INVALID = non-readable file
FILE_INVALID="/etc/shadow"



###
### MultiLineBuffer Test
### 

### Using `SAVEPATH` settings to test MultiLineBuffer:
###   - *usable-value condition: `os.path.isdir(value)`
###   - checking current *usable-value: ./phpsploit -e session | grep 'phpsploit.session'

### assert `SAVEPATH` is a MultiLineBuffer
phpsploit_pipe help set SAVEPATH > $TMPFILE || FAIL
assert_contains $TMPFILE 'is a MultiLineBuffer'

# display SAVEPATH value through another phpsploit command that uses it
function show_val_SAVEPATH () {
    phpsploit_pipe session | grep -oP '(?<=\()[a-z/]+(?=phpsploit.session\)$)'
}

### test SAVEPATH with valid directory
mkdir "$TMPFILE-valid-dir"
echo "$TMPFILE-valid-dir" > $IN
phpsploit_pipe set SAVEPATH + > $TMPFILE || FAIL
# buffer should contain the new value
phpsploit_pipe set SAVEPATH + > $TMPFILE || FAIL
assert_contains $OUT $TMPFILE-valid-dir
show_val_SAVEPATH > $TMPFILE && assert_contains $TMPFILE $TMPFILE-valid-dir

### test SAVEPATH with INVALID directory (old value should remain)
cat > $IN << EOF
$TMPFILE-invalid-dir
EOF
phpsploit_pipe set SAVEPATH + > $TMPFILE && FAIL
# buffer should STILL contain old value
phpsploit_pipe set SAVEPATH + > $TMPFILE || FAIL
assert_contains $OUT $TMPFILE-valid-dir
show_val_SAVEPATH > $TMPFILE && assert_contains $TMPFILE $TMPFILE-valid-dir

### Using `PAYLOAD_PREFIX` setting to test MultiLineBuffer:
###   - *usable-value condition: **NO-CONDITION**

### set PAYLOAD_PREFIX to a 8 lines buffer (with blank lines & comments)
cat > $IN << EOF
line1
# this is a comment, and next, 2 blank lines


line5
line6
line7
# another comment
EOF
perl -pe 'chomp if eof' $IN > $IN-2
phpsploit_pipe set PAYLOAD_PREFIX + > $TMPFILE || FAIL
# buffer should be exactly as defined in $IN
phpsploit_pipe set PAYLOAD_PREFIX + > $TMPFILE || FAIL
diff $OUT $IN-2 || FAIL
rm -f $IN-2
# PAYLOAD_PREFIX repr should say '8 lines':
phpsploit_pipe set PAYLOAD_PREFIX > $TMPFILE || FAIL
assert_contains $TMPFILE '<MultiLine@.* (8 lines)>$'

### set PAYLOAD_PREFIX to a SINGLE LINE BUFFER
echo 'SingleLineValue' > $IN
phpsploit_pipe set PAYLOAD_PREFIX + > $TMPFILE || FAIL
# PAYLOAD_PREFIX repr should simply show the value
phpsploit_pipe set PAYLOAD_PREFIX > $TMPFILE || FAIL
assert_contains $TMPFILE 'SingleLineValue'
assert_not_contains $TMPFILE << EOF
MultiLine
1 line
EOF

### set PAYLOAD_PREFIX to an EMPTY BUFFER
> $IN
phpsploit_pipe set PAYLOAD_PREFIX + > $TMPFILE || FAIL
# PAYLOAD_PREFIX repr should say '0 lines':
phpsploit_pipe set PAYLOAD_PREFIX > $TMPFILE || FAIL
assert_contains $TMPFILE '<MultiLine@d41d8cd98f00b204e9800998ecf8427e (0 lines)>'

### test 'set <SETTING> + <VALUE>' syntax
# bind to FILE_5LINES, check buffer is updated
phpsploit_pipe set PAYLOAD_PREFIX + file://$FILE_5LINES > $TMPFILE || FAIL
phpsploit_pipe set PAYLOAD_PREFIX > $TMPFILE || FAIL
assert_contains $TMPFILE "<MultiLine@$FILE_5LINES (5 lines)>$"

# add a line, unbinding the buffer from file:
phpsploit_pipe set PAYLOAD_PREFIX + line6 > $TMPFILE || FAIL
phpsploit_pipe set PAYLOAD_PREFIX > $TMPFILE || FAIL
assert_contains $TMPFILE "<MultiLine@[a-f0-9]\{32\} (6 lines)>$"

# bind if to FILE_INVALID, check buffer is kept
phpsploit_pipe set PAYLOAD_PREFIX + file://$FILE_INVALID > $TMPFILE || FAIL
phpsploit_pipe set PAYLOAD_PREFIX > $TMPFILE || FAIL
assert_contains $TMPFILE "<MultiLine@$FILE_INVALID (6 lines)>$"

# re-bind to FILE_5LINES, check buffer is updated
phpsploit_pipe set PAYLOAD_PREFIX + file://$FILE_5LINES > $TMPFILE || FAIL
phpsploit_pipe set PAYLOAD_PREFIX > $TMPFILE || FAIL
assert_contains $TMPFILE "<MultiLine@$FILE_5LINES (5 lines)>$"

# re-bind to FILE_EMPTY, check buffer is kept
phpsploit_pipe set PAYLOAD_PREFIX + file://$FILE_EMPTY > $TMPFILE || FAIL
phpsploit_pipe set PAYLOAD_PREFIX > $TMPFILE || FAIL
assert_contains $TMPFILE "<MultiLine@$FILE_EMPTY (5 lines)>$"

# add a line, unbinding the buffer from file:
phpsploit_pipe set PAYLOAD_PREFIX + line6 > $TMPFILE || FAIL
phpsploit_pipe set PAYLOAD_PREFIX > $TMPFILE || FAIL
assert_contains $TMPFILE "<MultiLine@[a-f0-9]\{32\} (6 lines)>$"

# reset to default value
phpsploit_pipe set PAYLOAD_PREFIX %%DEFAULT%% > $TMPFILE || FAIL
phpsploit_pipe set PAYLOAD_PREFIX > $TMPFILE || FAIL
assert_contains $TMPFILE "<MultiLine@[a-f0-9]\{32\} (16 lines)>$"

# FAIL to reset to FILE_EMPTY or FILE_INVALID
phpsploit_pipe set PAYLOAD_PREFIX file://FILE_EMPTY > $TMPFILE && FAIL
phpsploit_pipe set PAYLOAD_PREFIX file://FILE_INVALID > $TMPFILE && FAIL
phpsploit_pipe set PAYLOAD_PREFIX > $TMPFILE || FAIL
assert_contains $TMPFILE "<MultiLine@[a-f0-9]\{32\} (16 lines)>$"



###
### RandLineBuffer Test
### 

### Using `BACKDOOR` settings to test RandLineBuffer:
###   - *usable-value condition: `'%%PASSKEY' in value`
###   - checking current *usable-value: `./phpsploit -e 'exploit --get-backdoor'`

# assert `BACKDOOR` is a RandLineBuffer
phpsploit_pipe help set BACKDOOR > $TMPFILE || FAIL
assert_contains $TMPFILE 'is a RandLineBuffer'

# display BACKDOOR value through another phpsploit command that uses it
function show_val_BACKDOOR () {
    phpsploit_pipe exploit --get-backdoor
}

### test BACKDOOR with valid value
echo %%PASSKEY%%ValidValue > $IN
phpsploit_pipe set BACKDOOR + > $TMPFILE || FAIL
phpsploit_pipe set BACKDOOR + > $TMPFILE || FAIL
# buffer should contain the new value
assert_contains $OUT %%PASSKEY%%ValidValue
show_val_BACKDOOR > $TMPFILE && assert_contains $TMPFILE PHPSPL01TValidValue

### test BACKDOOR with INVALID value (old value should remain)
echo /invalid > $IN
phpsploit_pipe set BACKDOOR + > $TMPFILE && FAIL
phpsploit_pipe set BACKDOOR + > $TMPFILE || FAIL
# buffer should STILL contain old value
assert_contains $OUT %%PASSKEY%%ValidValue
show_val_BACKDOOR > $TMPFILE && assert_contains $TMPFILE PHPSPL01TValidValue

### set BACKDOOR to a 4 choices buffer (with blank lines & comments)
cat > $IN << EOF
choice1 %%PASSKEY%%
# this is a comment, and next, 2 blank lines


choice2 %%PASSKEY%%
choice3 %%PASSKEY%%
choice4 %%PASSKEY%%
# another comment %%PASSKEY%%
EOF
perl -pe 'chomp if eof' $IN > $IN-2
# shoud not fail
phpsploit_pipe set BACKDOOR + > $TMPFILE || FAIL
phpsploit_pipe set BACKDOOR + > $TMPFILE || FAIL
# buffer should be exactly as defined
diff $OUT $IN-2 || FAIL
rm -f $IN-2
# BACKDOOR repr should say '4 choices':
phpsploit_pipe set BACKDOOR > $TMPFILE || FAIL
assert_contains $TMPFILE '<RandLine@.* (4 choices)>$'
# try to show_val 50 times, and make sure all 4 choices where picked as *usable-value
buf=""
for i in {1..50}; do
    buf="$buf exploit --get-backdoor;"
done
phpsploit_pipe "$buf" | grep '^<?php' > $TMPFILE
assert_contains $TMPFILE << EOF
choice1
choice2
choice3
choice4
EOF
# assert not other choice has been picked as *usable-value
grep -qv 'choice[1-4] PHPSPL01T' $TMPFILE && FAIL

### set BACKDOOR to a SINGLE LINE BUFFER
echo 'SingleValue%%PASSKEY%%' > $IN
phpsploit_pipe set BACKDOOR + > $TMPFILE || FAIL
# BACKDOOR repr should simply show the value
phpsploit_pipe set BACKDOOR > $TMPFILE || FAIL
assert_contains $TMPFILE 'SingleValue%%PASSKEY%%'
assert_not_contains $TMPFILE << EOF
RandLine
1 choice
EOF

# set BACKDOOR to EMPTY BUFFER. should FAIL with:
#   'couldn't find an *usable-choice from buffer lines'
> $IN
phpsploit_pipe set BACKDOOR + > $TMPFILE && FAIL
assert_contains $TMPFILE "couldn't find an \*usable-choice from buffer lines"

### test 'set <SETTING> + <VALUE>' syntax
# bind to FILE_5LINES, check buffer is updated
phpsploit_pipe set BACKDOOR + file://$FILE_5LINES > $TMPFILE || FAIL
phpsploit_pipe set BACKDOOR > $TMPFILE || FAIL
assert_contains $TMPFILE "<RandLine@$FILE_5LINES (3 choices)>$"

# add an INVALID choice, unbinding the buffer from file:
phpsploit_pipe set BACKDOOR + invalidLine > $TMPFILE || FAIL
# check it's still 3 choices, as our line is not an *usable-choice
phpsploit_pipe set BACKDOOR > $TMPFILE || FAIL
assert_contains $TMPFILE "<RandLine@[a-f0-9]\{32\} (3 choices)>$"
# but check buffer actually has the last line
phpsploit_pipe set BACKDOOR + > /dev/null
tail -n1 $OUT | grep -q '^invalidLine$' || FAIL

# add an VALID choice:
phpsploit_pipe set BACKDOOR + validLine%%PASSKEY%% > $TMPFILE || FAIL
# check it's now 4 choices, because the added choice is an *usable-value
phpsploit_pipe set BACKDOOR > $TMPFILE || FAIL
assert_contains $TMPFILE "<RandLine@[a-f0-9]\{32\} (4 choices)>$"
# but check buffer actually has the last line
phpsploit_pipe set BACKDOOR + > /dev/null
tail -n1 $OUT | grep -q '^validLine' || FAIL

# bind to FILE_INVALID, check buffer is kept
phpsploit_pipe set BACKDOOR + file://$FILE_INVALID > $TMPFILE || FAIL
phpsploit_pipe set BACKDOOR > $TMPFILE || FAIL
assert_contains $TMPFILE "<RandLine@$FILE_INVALID (4 choices)>$"

# re-bind to FILE_5LINES, check buffer is updated
phpsploit_pipe set BACKDOOR + file://$FILE_5LINES > $TMPFILE || FAIL
phpsploit_pipe set BACKDOOR > $TMPFILE || FAIL
assert_contains $TMPFILE "<RandLine@$FILE_5LINES (3 choices)>$"

# re-bind to FILE_EMPTY, check buffer is kept
phpsploit_pipe set BACKDOOR + file://$FILE_EMPTY > $TMPFILE || FAIL
phpsploit_pipe set BACKDOOR > $TMPFILE || FAIL
assert_contains $TMPFILE "<RandLine@$FILE_EMPTY (3 choices)>$"

# reset to default value
phpsploit_pipe set BACKDOOR %%DEFAULT%% > $TMPFILE || FAIL
phpsploit_pipe set BACKDOOR > $TMPFILE || FAIL
assert_contains $TMPFILE "HTTP_%%PASSKEY%%"

# FAIL to reset to FILE_EMPTY or FILE_INVALID
phpsploit_pipe set BACKDOOR file://FILE_EMPTY > $TMPFILE && FAIL
phpsploit_pipe set BACKDOOR file://FILE_INVALID > $TMPFILE && FAIL
phpsploit_pipe set BACKDOOR > $TMPFILE || FAIL
# check buffer still the same as before (%%DEFAULT%%)
assert_contains $TMPFILE "HTTP_%%PASSKEY%%"
