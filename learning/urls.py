from django.conf.urls import patterns, include, url
from django.contrib import admin
from blog.feeds import PostFeed


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'learning.views.home', name='home'),
    # url(r'^learning/', include('learning.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^markdown/', include('django_markdown.urls')),
    url(r'^$', 'blog.views.post_index'),
    url(r'^post/(?P<slug>[a-zA-Z0-9_\-]+)\.html$', 'blog.views.post'),
    url(r'^tag/(?P<slug>[a-zA-Z0-9_\-]+)/$', 'blog.views.tag'),
    url(r'^tags/$', 'blog.views.tag_index'),
    url(r'^message/$', 'blog.views.leave_message'),

    url(r'^tools/qrcode/$', 'blog.views.generate_qrcode'),
    url(r'^tools/video-resolve/', 'blog.views.video_resolve'),
    url(r'^tools/webp-check/$', 'blog.views.webp_check'),

    url(r'^links/$', 'blog.views.link_index'),

    url(r'^feeds/(?P<url>.*)/$', PostFeed()),
)
