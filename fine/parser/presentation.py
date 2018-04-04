import os
import re
import yaml
from .frame import Frame


class PATTERN(object):

    SEP = re.compile(r'^(-{3,})$')
    META = re.compile(r'^(\.{3,})$')


class Presentation(object):
    
    def __init__(self, **kwargs):
        self.frames = []
        self.meta = None
        if 'extensions' in kwargs:
            self.extensions = kwargs.pop('extensions')
        else:
            self.extensions = []

    def __repr__(self):
        REPR = "Fine Presentation: \n"
        for key, val in self.meta.items():
            REPR += "    %s: %s\n" % (key, val)
        REPR += "    frames: %d" % (len(self.frames), )
        return REPR

    def parse(self, text):
        text = text.strip()

        while text:
            meta, content, text = self.parse_block(text)
            meta = yaml.load(meta)
            self.load_markdown(meta)
            self.load_frame(meta, content)
        first = self.frames.pop(0)
        self.meta = first.configs

    def parse_block(self, text):
        meta = ''
        content = ''

        text = text.lstrip()
        lines = text.splitlines()

        first_line = lines.pop(0)
        m = re.match(PATTERN.SEP, first_line.rstrip())
        if m is None:
            raise ValueError("Missing Frame Seperator around %s" % first_line)

        stack = []
        while lines:
            m = re.match(PATTERN.SEP, lines[0].rstrip())
            if m is not None:
                break

            line = lines.pop(0)
            m = re.match(PATTERN.META, line.rstrip())
            if m is not None:
                meta = '\n'.join(stack)
                stack.clear()
            else:
                stack.append(line)

        content = '\n'.join(stack)
        text = '\n'.join(lines)
        return meta, content, text


    def load_markdown(self, meta):
        if meta is not None and 'markdown' in meta:
            if 'extensions' in meta['markdown']:
                self.extensions.extend(meta['markdown']['extensions'])

    def load_frame(self, meta, content):
        if meta is None:
            self.frames.append(
                Frame(content, extensions=self.extensions)
            )
        else:
            self.frames.append(
                Frame(content, extensions=self.extensions, **meta)
            )
