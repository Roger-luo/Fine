import markdown
from .html_attrs import HTMLAttr


class data(HTMLAttr):

    prefix = 'data'
    elements = ['transition']


class background(HTMLAttr):

    prefix = 'data-background'
    elements = ['color', 'image', 'size', 'position']


class transition(HTMLAttr):

    prefix = 'data-transition'
    elements = ['speed']


class Frame(object):

    def __init__(self, text, **kwargs):
        self.text = text.strip()
        self.configs = kwargs

    @property
    def html(self):
        if 'extensions' in self.configs:
            extensions = self.configs['extensions']
        else:
            extensions = []
        html = markdown.markdown(self.text, extensions=extensions)
        return html

    @property
    def note(self):
        if 'note' in self.configs:
            return self.configs['note']
        return ''

    @property
    def attrs(self):
        if self.configs is None:
            return ''

        html_attrs = dict()
        for each in HTMLAttr.__subclasses__():
            html_attrs[each.__name__] = each

        attrs = []
        for key in html_attrs:
            if key in self.configs:
                attrs.append(html_attrs[key](**self.configs[key]))
        
        return ' '.join(str(each) for each in attrs)

    def dump(self):
        return "<section %s>\n%s\n<\section>" % (self.attrs, self.html)

    def __repr__(self):
        return self.dump()
