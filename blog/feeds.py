# coding=utf8
from django.contrib.syndication.views import Feed
from blog.models import Post
from utils.markdown_util import MarkdownUtil


class PostFeed(Feed):
    title = '学习小站 - 技术学习与思考'
    link = '/feeds/posts/'
    description = '技术学习与思考小站'

    def items(self):
        return Post.objects.order_by('-created')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return MarkdownUtil.convert(item.content)

    def item_link(self, item):
        return item.get_absolute_url()
