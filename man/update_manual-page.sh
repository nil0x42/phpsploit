#!/bin/bash

txt2tags -t man \
    -i manual-page.txt2tags \
    -o phpsploit.1

### DEPRECATED PART OF THE SCRIPT:
### The README file is now different than the MANPAGE

# MANWIDTH=80 man \
#     -P cat man/phpsploit.1 \
#     > README
