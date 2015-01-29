# coding=utf8
import markdown
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.codehilite import CodeHiliteExtension


class MarkdownUtil(object):

    md = markdown.Markdown(extensions=[FencedCodeExtension(), CodeHiliteExtension()])

    @classmethod
    def convert(cls, *args, **kwargs):
        return cls.md.convert(*args, **kwargs)
