from django.contrib import admin
from django_markdown.admin import MarkdownModelAdmin
from blog.models import *

admin.site.register(Post, MarkdownModelAdmin)
admin.site.register(Tag)
admin.site.register(Quote)
