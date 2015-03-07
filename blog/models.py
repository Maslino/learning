# coding=utf8
import random
from django.db import models
from django.core.validators import RegexValidator
from django_markdown.models import MarkdownField


class Post(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.CharField(max_length=255, unique=True, validators=[RegexValidator(r'[a-zA-Z0-9_\-]+')])
    content = MarkdownField()
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