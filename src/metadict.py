"""Advanced dict-like classes for processing phpsploit
complex session objects.
"""
__all__ = ["MetaDict", "VarContainer"]

from ui.color import colorize
from utils.regex import WORD_TOKEN


class MetaDict(dict):
    """MetaDict() object

    An advanced dict() like class with advanced features,
    for phpsploit session objects.

    Metadict() can be instanciated from a built-in dict().
    Otherwise, it instanciates itself as en empty directory.

    Magic item access
    -----------------
    The _isattr() method is used as pattern syntax validator on
    __getattribute__() and __setattr__() methods in order to
    respectively use __getitem__() and __setitem__() magic methods
    instead.
    Defaultly, the _isattr() function returns False anyway. This
    means that this nice feature is disabled until overwritten
    by some child class.

    Example:
    An hypothetical child class may enable the item access feature
    explained above by rewritting the _isattr() method like this:
    >>> def _isattr(self, name):
    ...     return name == name.capitalize()

    This way, any called instance attribute whose name is in
    capitalized format will be automagically linked to the self
    dict's corresponding item name, like in the folowing
    concrete case:
    >>> obj = MetaDict({'Foo':'bar', 'baz':'qux'})
    # items whose name _isattr() can be accessed as attributes:
    >>> assert obj["Foo"]` == obj.Foo
    # in this example, 'baz' doesn't match _isattr() (capitalize())
    >>> assert obj["baz"] != obj.baz

    Dynamic block display
    ---------------------
    This base class provides a nice dynamic columnized multiline
    string representation of the self dict items. This behavior
    is managed by the __call__() magic method.
    The optionnal argument `pattern` can be used to limit
    item display to keys whose name starts with it's value.
    When displayed, the output string uses self __doc__'s first
    line as title unless alternative title had been provided as
    __init__() named optionnal argument.

    If the self dict does not contains any item, or the pattern
    filter does not match any item name, a ValueError is raised.

    NOTE: Calling the magic __str__() method returns the __call__()
          string result (without `pattern` argument.

    """

    # pylint: disable=super-init-not-called
    def __init__(self, value=None, title=None):
        if value is None:
            value = {}
        self.update(value)

        if title is None:
            if self.__doc__:
                self.title = self.__doc__.splitlines()[0].strip()
            else:
                self.title = "%s() object" % self.__class__.__name__
        else:
            self.title = str(title)

    def __getattribute__(self, name):
        if name != "_isattr" and self._isattr(name):
            return self.__getitem__(name)
        return super().__getattribute__(name)

    def __setattr__(self, name, value):
        if self._isattr(name):
            return self.__setitem__(name, value)
        return super().__setattr__(name, value)

    def __dir__(self):
        """considering the special get/set behavior, __dir__() method
        shall also return self item whose name matches self._isattr().
        """
        return super().__dir__() + [i for i in self.keys() if self._isattr(i)]

    def _isattr(self, name): # pylint: disable=unused-argument,no-self-use
        """Determine whether a called attribute name may be
        considered as an item call. By default, it returns False
        anyway, disabling that feature.
        """
        return False

    def __str__(self):
        """Return self __call__() method"""
        return self.__call__()

    def __call__(self, pattern=""):
        """Display self dict's items as a formatted multiline string array.
        The optionnal argument `pattern` is an optional prefix to only
        display matching items.
        """
        # get matching vars list
        sing_title = self.title
        if sing_title.endswith("s"):
            sing_title = sing_title[:-1]
        if not self.keys():
            raise ValueError("No such " + sing_title)
        keys = [k for k in self.keys() if k.startswith(pattern)]
        if not keys:
            msg = "No {} matching «{}»"
            raise ValueError(msg.format(sing_title, pattern))

        tpl = ("    {:%s}  {}\n") % max(8, len(max(keys, key=len)))
        buffer = self.title + "\n" + ("=" * len(self.title)) + "\n\n"
        buffer += tpl.format("Variable", "Value")
        buffer += tpl.format("--------", "-----")
        for idx, key in enumerate(sorted(keys)):
            buffer += colorize(["%Reset", "%Reset"][idx % 2],
                               tpl.format(key, self[key]))
        return "\n" + buffer + colorize("%Reset")

    def update(self, new_dict):
        """Override parent (dict.update()), because it seems that
        built-in method doesn't use self.__setitem__() internally,
        which is problematic for phpsploit
        """
        if isinstance(new_dict, dict):
            for key, value in new_dict.items():
                self[key] = value
        else:
            super().update(new_dict)


class VarContainer(MetaDict):
    """VarContainer() object

    This class unherits Metadict, and just implements a way to delete
    items by settings them to a set of magic values (item_deleters)

    >>> obj = VarContainer()
    >>> obj['KEY'] = "foobar"
    >>> # in this objects, the two following lines do exactly the same thing:
    >>> del obj['KEY']
    >>> obj['KEY'] = "None"
    """
    item_deleters = ["", "NONE"]

    def __setitem__(self, name, value):
        """If `value` is None, "None" (case-insensitive) or "" (empty str),
        the item is removed instead of being reassigned.

        This behavior allows the user to easily remove settings,
        env-vars, aliases, and any object unheriting this class,
        by simply assiging None to them.

        It also raises a KeyError if value is not a valid WORD_TOKEN
        """
        if isinstance(value, (str, type(None))) and \
                str(value).upper() in self.item_deleters:
            if name not in self.keys():
                return None
            return self.__delitem__(name)
        if not WORD_TOKEN.fullmatch(name):
            raise KeyError("illegal name: %r doesn't match %s"
                           % (name, WORD_TOKEN.pattern))
        return super().__setitem__(name, value)
