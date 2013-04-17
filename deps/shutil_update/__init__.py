"""Phpsploit's shutil_upgrade patch imports all needed shutil functions
and attributes that are not available before python3.3

"""
import shutil

def needs(*attrs):
    for attr in attrs:
        if not hasattr(shutil, attr):
            module = getattr(__import__('shutil_new'), attr)
            setattr(shutil, attr, module)

# make those functions available from standard shutil
needs('which', 'get_terminal_size')
