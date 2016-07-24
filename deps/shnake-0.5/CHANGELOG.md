### Version 0.5 *(2016-07-24)*
- fix return_errcode() handler for boolean values.
- make lexer source code PEP8 compliant.

### Version 0.4 *(2014-10-25)*
- `command not found` now returns 127, just like bash
- interpret() now supports bash's 'set -e' like behavior,
  by setting `fatal_errors` argument to True.

### Version 0.3 *(2014-07-31)*
- Remove implicit call of `help <cmd>` when typing `<cmd> --help`.
- Add **CHANGELOG.md** file.

### Version 0.2 *(2014-07-31)*
- Convert **README** file to markdown format.
- Improve **demo.py** file
- Fix some minor bugs on **shell.py**

### Version 0.1 *(2014-04-15)*
- First release.
