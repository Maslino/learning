# coding=utf8
import random
import traceback
import xmlrpclib
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django_markdown.models import MarkdownField
from django.db.models.signals import post_save
from django.dispatch import receiver
from utils.markdown_util import MarkdownUtil
from learning.settings import BAIDU_PING_SERVICE, SITE_URL, SITE_NAME


class Post(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.CharField(max_length=255, unique=True, validators=[RegexValidator(r'[a-zA-Z0-9_\-]+')])
    content = MarkdownField()
    author = models.ForeignKey(User)
    visited = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tag', db_table='post_tag_rel')
    # todo: comments

    def __unicode__(self):
        return self.title

    @property
    def prev_post(self):
        return Post.objects.filter(id__lt=self.id).order_by('-id').first()

    @property
    def next_post(self):
        return Post.objects.filter(id__gt=self.id).order_by('id').first()

    def get_absolute_url(self):
        return '/post/' + self.slug + '.html'

    def get_html(self):
        return MarkdownUtil(self.content).get_html()


class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.CharField(max_length=64, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    @property
    def related_posts(self):
        return Post.objects.filter(tags__in=[self])

    def get_absolute_url(self):
        return '/tag/' + self.slug + '/'


class Quote(models.Model):
    content = models.TextField()
    author = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.content

    @classmethod
    def random_get(cls):
        count = cls.objects.all().aggregate(count=models.Count('id'))['count']
        if count == 0:
            return None
        times = 3
        while times > 0:
            try:
                index = random.randint(0, count - 1)
                return cls.objects.all()[index]
            except IndexError:
                times -= 1


class File(models.Model):
    upload_file = models.FileField(upload_to='%Y/%m/%d', max_length=255)

    def __unicode__(self):
        return self.upload_file.url


class Link(models.Model):
    name = models.CharField(max_length=256)
    url = models.URLField(max_length=512)
    category = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'[' + unicode(self.category) + u']' + unicode(self.name)


@receiver(post_save, sender=Post)
def ping_baidu(sender, **kwargs):
    post = kwargs.get('instance')
    if not post:
        return
    try:
        proxy = xmlrpclib.ServerProxy(BAIDU_PING_SERVICE)
        response = proxy.weblogUpdates.extendedPing(
            SITE_NAME,
            SITE_URL,
            SITE_URL + post.get_absolute_url(),
            SITE_URL + '/feeds/posts/'
        )
        print 'response from baidu ping:', response
    except Exception:
        traceback.print_exc()
