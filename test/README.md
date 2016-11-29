# UNIT TESTS

# Usage:
    ./test/RUN.sh
    ./test/RUN.sh -h

# About:
    * The test launcher runs all tests in directory, in a recursive manner.

    * For a given directory:
        If 'PRE_TEST.sh' exists, it is run before all other scripts
        If 'POST_TEST.sh' exists, it is run after all other scripts
        A file must be executable to be run by the launcher
