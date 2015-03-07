from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'learning.views.home', name='home'),
    # url(r'^learning/', include('learning.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^markdown/', include('django_markdown.urls')),
    url(r'^$', 'blog.views.index'),
    url(r'^post/(?P<slug>[a-zA-Z0-9_\-]+)\.html$', 'blog.views.post'),
    url(r'^tag/(?P<slug>[a-zA-Z0-9_\-]+)/$', 'blog.views.tag'),
)
