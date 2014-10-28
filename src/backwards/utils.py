"""Misc functions useful for backwards loaders.

"""


def rename_key(dictionnary, old_keyname, new_keyname):
    if old_keyname in dictionnary:
        dictionnary[new_keyname] = dictionnary.pop(old_keyname)


def remove_key(dictionnary, keyname):
    if keyname in dictionnary.keys():
        del dictionnary[keyname]
