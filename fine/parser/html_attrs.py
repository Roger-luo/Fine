class HTMLAttrMeta(type):
    """meta class for creating properties.

    properties registed in elements will be created
    in subclass.
    """

    def __new__(cls, name, bases, attrs):

        elements = attrs['elements']
        prefix = attrs['prefix']
        for each in elements:
            HTMLAttrMeta.addattr(attrs, each, prefix)
        return type.__new__(cls, name, bases, attrs)

    def attr2str(attr):
        if 'val' in attr:
            return "%s=\"%s\"" % (attr['name'], attr['val'])
        else:
            return ''

    def addattr(attrs, name, prefix):
        def getter(self):
            return HTMLAttrMeta.attr2str(getattr(self, '_' + name))

        def setter(self, val):
            attr = getattr(self, '_' + name)
            attr['val'] = val

        if prefix:
            fullname = prefix + '-' + name
        else:
            fullname = name
        attrs['_' + name] = {'name': fullname}
        attrs[name] = property(
            fget=getter,
            fset=setter,
        )


class HTMLAttr(object, metaclass=HTMLAttrMeta):
    """A Python Wrapper for HTML Attributes.

    Subclassing this base class will creates related
    attributes wrapper.

    Example:

    class data(HTMLAttr):

        prefix = 'data'
        elements = ['transition']

    creates a string 'data-transition=fade' when trying to
    use this its instance as a string.

    all its subclass will be initialized by keys in elements
    """

    prefix = ''
    elements = []

    def __init__(self, **meta):
        for key, val in meta.items():
            if getattr(self, key, None) is not None:
                setattr(self, key, val)

    def __repr__(self):
        content = []
        for each in self.elements:
            val = getattr(self, each)
            if val:
                content.append(val)
        return ' '.join(content)
