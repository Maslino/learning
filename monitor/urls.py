from django.conf.urls import patterns, url


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'learning.views.home', name='home'),
    # url(r'^learning/', include('learning.urls')),

    url(r'^verify/$', 'monitor.api.verify'),
)
