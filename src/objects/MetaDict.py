from ui.color import colorize


class MetaDict(dict):
    """Metadict() object (by nil0x42)

    Instanciate an advanced dict() like datatype, especially
    made in order to extend PhpSploit session management taste.

    It may take a dict based object as argument to bind to it.
    Otherwise, it instanciates itself as an empty dictionnary set.


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
    >>> `obj["Foo"]` == `obj.Foo` # those calls are identical
    >>> `obj["baz"]` != `obj.baz` # "baz" != "baz".capitalize()


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

    def __init__(self, value={}, title=None):
        # default title
        self.title = "Metadict() object (by nil0x42)"
        # update self dict with `value`
        self.update(value)

        # get object's title string
        if title is not None:
            self.title = str(title)
        else:
            try:
                self.title = self.__doc__.splitlines()[0].strip()
            except:
                self.title = "%s() object" % self.__class__.__name__

    def __getattribute__(self, name):
        # if _isattr(name), then call self getitem
        if name != "_isattr" and self._isattr(name):
            return self.__getitem__(name)

        # otherwise call parent's getattribute
        return super().__getattribute__(name)

    def __setattr__(self, name, value):
        # if _isattr(name), then call self setitem
        if self._isattr(name):
            return self.__setitem__(name, value)

        # otherwise call parent's setattr
        return super().__setattr__(name, value)

    def __dir__(self):
        # considering the special get/set behavior, the __dir__()
        # method must also return self item whose name complies
        # with the self _isattr() boolean function.
        return super().__dir__() + [i for i in self.keys() if self._isattr(i)]

    def _isattr(self, name):
        """Determine whether a called attribute name may be
        considered as an item call. By default, it returns False
        anyway, disabling that feature.

        """
        return False

    def __str__(self):
        """Return self __call__() method"""
        return self.__call__()

    def __call__(self, pattern=""):
        """Nicely display self dict's items as a formatted
        multiline string array.
        The optionnal argument `pattern` can be used to limit
        item display to keys whose name starts with it's value.

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

        # process formatted string
        tpl = ("    {:%s}  {}\n") % max(8, len(max(keys, key=len)))

        buffer = self.title + "\n" + ("=" * len(self.title)) + "\n\n"

        buffer += tpl.format("Variable", "Value")
        buffer += tpl.format("--------", "-----")

        for id, key in enumerate(sorted(keys)):
            buffer += colorize(["%Reset", "%Reset"][id % 2],
                               tpl.format(key, self[key]))

        return "\n" + buffer + colorize("%Reset")

    def update(self, new):
        """Override standard dict() update method, because it seems
        that using the default one does not use self object's
        __setitem__() method. This is problematic for phpsploit
        session main objects.
        """
        # let parent handle exception if not a dict
        if not isinstance(new, dict):
            return super().update(new)
        # replace each self item using standard setitem method
        for key, value in new.items():
            self[key] = value
