# coding=utf8
import markdown


class MarkdownUtil(object):

    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.fenced_code',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            ])

    @classmethod
    def convert(cls, *args, **kwargs):
        return cls.md.convert(*args, **kwargs)
