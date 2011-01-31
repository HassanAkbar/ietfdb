from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'sec.drafts.views.search', name='drafts_search'),
    url(r'^add/$', 'sec.drafts.views.add', name='drafts_add'),
    url(r'^dates/$', 'sec.drafts.views.dates', name='drafts_dates'),
    url(r'^(?P<id>\d{1,6})/$', 'sec.drafts.views.view', name='drafts_view'),
    url(r'^(?P<id>\d{1,6})/abstract/$', 'sec.drafts.views.abstract', name='drafts_abstract'),
    url(r'^(?P<id>\d{1,6})/announce/$', 'sec.drafts.views.announce', name='drafts_announce'),
    url(r'^(?P<id>\d{1,6})/authors/$', 'sec.drafts.views.authors', name='drafts_authors'),
    url(r'^(?P<id>\d{1,6})/confirm/$', 'sec.drafts.views.confirm', name='drafts_confirm'),
    url(r'^(?P<id>\d{1,6})/edit/$', 'sec.drafts.views.edit', name='drafts_edit'),
    url(r'^(?P<id>\d{1,6})/extend/$', 'sec.drafts.views.extend', name='drafts_extend'),
    url(r'^(?P<id>\d{1,6})/email/$', 'sec.drafts.views.email', name='drafts_email'),
    url(r'^(?P<id>\d{1,6})/makerfc/$', 'sec.drafts.views.makerfc', name='drafts_makerfc'),
    url(r'^(?P<id>\d{1,6})/replace/$', 'sec.drafts.views.replace', name='drafts_replace'),
    url(r'^(?P<id>\d{1,6})/resurrect/$', 'sec.drafts.views.resurrect', name='drafts_resurrect'),
    url(r'^(?P<id>\d{1,6})/revision/$', 'sec.drafts.views.revision', name='drafts_revision'),
    url(r'^(?P<id>\d{1,6})/update/$', 'sec.drafts.views.update', name='drafts_update'),
    url(r'^(?P<id>\d{1,6})/withdraw/$', 'sec.drafts.views.withdraw', name='drafts_withdraw'),
)
