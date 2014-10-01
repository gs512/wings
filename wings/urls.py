from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wings.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^library/', include('library.urls')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'library/login.html'}),
)
