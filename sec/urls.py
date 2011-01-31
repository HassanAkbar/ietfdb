from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    url(r'^$', direct_to_template, {'template': 'main.html'}, name="home"),
    (r'^admin/', include(admin.site.urls)),
    (r'^areas/', include('sec.areas.urls')),
    (r'^drafts/', include('sec.drafts.urls')),
    (r'^groups/', include('sec.groups.urls')),
    (r'^liaison/', include('sec.liaison.urls')),
    (r'^roles/', include('sec.roles.urls')),
    (r'^rolodex/', include('sec.rolodex.urls')),
    (r'^interim/', include('sec.interim.urls')),
    (r'^proceedings/', include('sec.proceedings.urls')),
)
