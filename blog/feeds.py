# coding=utf8
from django.contrib.syndication.views import Feed
from blog.models import Post


class PostFeed(Feed):
    title = '学习小站 - 技术学习与思考'
    link = '/feeds/posts/'
    description = '技术学习与思考小站'

    def items(self):
        return Post.objects.order_by('-created')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.get_html()

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.created

    def item_author_name(self, item):
        return item.author.username
