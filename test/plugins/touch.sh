#!/bin/bash

# connect phpsploit
phpsploit_pipe exploit > $TMPFILE

# permission denied
phpsploit_pipe touch /etc/shadow > $TMPFILE && FAIL
assert_contains $TMPFILE "Permission denied"

# no such file or directory
phpsploit_pipe touch /laskdjlsakjdlaskjd/notexist > $TMPFILE && FAIL
assert_contains $TMPFILE "No such file or directory"

# touch directory (must work)
phpsploit_pipe stat . > $TMPFILE-before || FAIL
sleep 1
phpsploit_pipe touch . > $TMPFILE || FAIL
phpsploit_pipe stat . > $TMPFILE-after || FAIL
diff $TMPFILE-before $TMPFILE-after > $TMPFILE-diff && FAIL
< $TMPFILE-diff grep '^>' > $TMPFILE
assert_contains $TMPFILE << EOF
 Accessed: 
 Modified: 
EOF

# touch existing file
phpsploit_pipe touch index.php > $TMPFILE || FAIL

# touch existing file with invalid `ref` file
phpsploit_pipe touch -r notexist index.php > $TMPFILE && FAIL
assert_contains $TMPFILE 'cannot stat.*notexist.*No such file'

# touch existing file with existing `ref` file
phpsploit_pipe touch -r index.php newfile.txt > $TMPFILE || FAIL
phpsploit_pipe stat index.php > $TMPFILE-before || FAIL
phpsploit_pipe stat newfile.txt > $TMPFILE-after || FAIL
diff $TMPFILE-before $TMPFILE-after > $TMPFILE-diff && FAIL

# touch file with -t (partial timestamp)
phpsploit_pipe touch -t 2015 index.php > $TMPFILE || FAIL
phpsploit_pipe stat index.php > $TMPFILE || FAIL
# year must be set to 2015
grep -q ' 2015-' $TMPFILE || FAIL
# hh:mm:ss must NOT be set to 00:00:00 (should be random)
grep -q '00:00:00' $TMPFILE && FAIL

# run touch with invalid arg
phpsploit_pipe touch --invalid-arg FOOBAR > $TMPFILE && FAIL
