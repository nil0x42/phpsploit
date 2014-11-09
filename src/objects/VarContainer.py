import objects


class VarContainer(objects.MetaDict):
    """VarContainer() object (by nil0x42)

    This class unherits objects.Metadict, and juste implements
    a specific flavour in the __setitem__() magic method:

    >>> obj = VarContainer()
    >>> obj['KEY'] = "foobar"
    >>> # in this objects, the two following lines do exactly the same thing:
    >>> del obj['KEY']
    >>> obj['KEY'] = "None"

    NOTES:
    Setting the key to None or "" (empty str) deletes it only according
    to `self.item_deleters`.
    This attribute can be set to something else in order to change behavior.

    """
    item_deleters = ["", "NONE"]

    def __init__(self, value={}, title=None):
        super().__init__(value, title)

    def __setitem__(self, name, value):
        """Unlike parent class MetaDict, setting an item/attribute
        with a None value, an empy string, or the "none" string
        removes the item instead of setting it to the wanted value.

        This behavior eases core implementation of environment,
        aliases, and any phpsploit var container designed for
        interactive use.

        """
        # delete item if its value is empty or None:
        if isinstance(value, (str, type(None))) and \
                str(value).upper() in self.item_deleters:
            # don't try to delete unexisting item
            if name not in self.keys():
                return
            return self.__delitem__(name)

        return super().__setitem__(name, value)
