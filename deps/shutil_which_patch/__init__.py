"""Since the 'which' function from 'shutil' module is not available on
Pyhon 3 < 3.3, we include it if unavailable.

which.py contains the which function from shutil module since python
3.3, it is under python license.

"""

import shutil
if not hasattr(shutil, 'which'):
    from .which import which
    shutil.which = which
