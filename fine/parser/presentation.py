import os
import re
import yaml
from .frame import Frame


class PATTERN(object):

    META = re.compile(r'^(-{3,})([\S\s]*?)(\.{3,})')
    FRAME = re.compile(r'^(-{3,})([\S\s]*?)(-{3,}|$)')


class Presentation(object):
    
    def __init__(self, text, **kwargs):
        text = text.strip()
        if 'extensions' in kwargs:
            self.extensions = kwargs.pop('extensions')
        else:
            self.extensions = []

        self.meta, text = self.parse_meta(text)
        self.frames, text = self.parse_frame(text)
        
    def __repr__(self):
        REPR = "Fine Presentation: \n"
        for key, val in self.meta.items():
            REPR += "    %s: %s\n" % (key, val)
        REPR += "    frames: %d" % (len(self.frames), )
        return REPR

    def parse_meta(self, text):
        m = re.match(PATTERN.META, text)
        if m is not None:
            meta = yaml.load(m.group(2))
            text = text[len(m.group(0)):]
        else:
            meta = {}
        return meta, text

    def parse_frame(self, text):
        frames = []

        while text:
            text = text.lstrip()
            m = re.match(PATTERN.FRAME, text)
            if m is None:
                raise ValueError('Frame should be seperated by ---')

            if m is not None:
                raw_frame = ''.join([m.group(1), m.group(2)])
                meta = re.match(PATTERN.META, raw_frame)
                content = m.group(2)
                if meta is None:
                    frames.append(Frame(content, extensions=self.extensions))
                else:
                    kwargs = yaml.load(meta.group(2))
                    raw_meta = ''.join([meta.group(2), meta.group(3)])
                    if 'extensions' in kwargs:
                        self.extensions.extend(kwargs.pop('extensions'))
                    frames.append(
                        Frame(
                            content[len(raw_meta):],
                            extensions=self.extensions,
                            **kwargs
                        )
                    )

                if m.group(3) == "":
                    text = text[len(m.group(0)):]
                else:
                    text = text[len(m.group(0))-3:]

        return frames, text
