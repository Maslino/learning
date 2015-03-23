# coding=utf8
import markdown


class MarkdownUtil(object):

    def __init__(self, content):
        """
        :param content: markdown content
        :return:
        """
        self.md = markdown.Markdown(
            extensions=[
                'markdown.extensions.fenced_code',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ],
        )
        self.html = self.md.convert(content)

    def get_html(self):
        return self.html

    def get_toc(self):
        """
        如果toc没有内容，md.toc返回
        <div class="toc">
        <ul></ul>
        </div>
        :return:
        """
        toc = self.md.toc
        if '<li>' not in toc:
            return None
        return toc


if __name__ == "__main__":
    print MarkdownUtil('abc').get_toc()
