from django.contrib import admin
from django_markdown.admin import MarkdownModelAdmin
from blog.models import *


class PostAdmin(MarkdownModelAdmin):
    fields = ('title', 'slug', 'author', 'content', 'tags')
    filter_horizontal = ('tags', )


admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Quote)
admin.site.register(File)
admin.site.register(Link)
