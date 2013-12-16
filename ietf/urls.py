# Copyright The IETF Trust 2007, 2009, All Rights Reserved

from django.conf.urls import patterns, include, handler404, handler500
from django.contrib import admin
from django.views.generic import RedirectView, TemplateView

from ietf.liaisons.sitemaps import LiaisonMap
from ietf.ipr.sitemaps import IPRMap

from django.conf import settings

admin.autodiscover()

# sometimes, this code gets called more than once, which is an
# that seems impossible to work around.
try:
    admin.site.disable_action('delete_selected')
except KeyError:
    pass

from dajaxice.core import dajaxice_autodiscover
dajaxice_autodiscover()

sitemaps = {
    'liaison': LiaisonMap,
    'ipr': IPRMap,
}

urlpatterns = patterns('',
    (r'^$', 'ietf.doc.views_search.frontpage'),
    (r'^accounts/', include('ietf.ietfauth.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^ann/', include('ietf.nomcom.redirect_ann_urls')),
    (r'^community/', include('ietf.community.urls')),
    (r'^cookies/', include('ietf.cookies.urls')),
    (r'^doc/', include('ietf.doc.urls')),
    (r'^drafts/', include('ietf.doc.redirect_drafts_urls')),
    (r'^feed/comments/(?P<remainder>.*)/$', RedirectView.as_view(url='/feed/document-changes/%(remainder)s/')),
    (r'^feed/', include('ietf.feed_urls')),
    (r'^help/', include('ietf.help.urls')),
    (r'^idtracker/', include('ietf.doc.redirect_idtracker_urls')),
    (r'^iesg/', include('ietf.iesg.urls')),
    (r'^ipr/', include('ietf.ipr.urls')),
    (r'^liaison/', include('ietf.liaisons.urls')),
    (r'^list/', include('ietf.mailinglists.urls')),
    (r'^meeting/', include('ietf.meeting.urls')),
    (r'^group/', include('ietf.group.urls')),
    (r'^person/', include('ietf.person.urls')),
    (r'^release/$', 'ietf.release.views.release'),
    (r'^release/(?P<version>.+)/$', 'ietf.release.views.release'),
    (r'^secr/', include('ietf.secr.urls')),
    (r'^sitemap-(?P<section>.+).xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.index', { 'sitemaps': sitemaps}),
    (r'^submit/', include('ietf.submit.urls')),
    (r'^sync/', include('ietf.sync.urls')),
    (r'^wg/', include('ietf.wginfo.urls')),
    (r'^stream/', include('ietf.group.stream_urls')),
    (r'^nomcom/', include('ietf.nomcom.urls')),
    (r'^templates/', include('ietf.dbtemplate.urls')),

    # Redirects
    (r'^(?P<path>public)/', include('ietf.redirects.urls')),

    # Google webmaster tools verification url
    (r'^googlea30ad1dacffb5e5b.html', TemplateView.as_view(template_name='googlea30ad1dacffb5e5b.html')),
    (r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
)

if settings.SERVER_MODE in ('development', 'test'):
    urlpatterns += patterns('',
        (r'^(?P<path>(?:images|css|js)/.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        (r'^(?P<path>secretariat/(img|css|js)/.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        (r'^(?P<path>robots\.txt)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT+"dev/"}),
        (r'^_test500/$', lambda x: None),
        (r'^environment/$', 'ietf.help.views.environment'),
	)
