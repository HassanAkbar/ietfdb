# Copyright The IETF Trust 2007, All Rights Reserved

from django.conf.urls import patterns
from django.views.generic import RedirectView

from ietf.meeting import views
from ietf.meeting import ajax

urlpatterns = patterns('',
    (r'^(?P<meeting_num>\d+)/materials.html$', views.materials),
    (r'^agenda/$', views.agenda),
    (r'^agenda(-utc)?(?P<ext>.html)?$', views.agenda),
    (r'^agenda(?P<ext>.txt)$', views.agenda),
    (r'^agenda(?P<ext>.csv)$', views.agenda),
    (r'^agenda/edit$', views.edit_agenda),
    (r'^requests.html$', RedirectView.as_view(url='/meeting/requests', permanent=True)),
    (r'^requests$', views.meeting_requests),
    (r'^agenda/agenda.ics$', views.ical_agenda),
    (r'^agenda.ics$', views.ical_agenda),
    (r'^agenda/week-view.html$', views.week_view),
    (r'^week-view.html$', views.week_view),
    (r'^(?P<num>\d+)/agenda/(?P<owner>[A-Za-z0-9-.+_]+@[A-Za-z0-9._]+)/(?P<name>[A-Za-z0-9-:_]+)/edit$', views.edit_agenda),
    (r'^(?P<num>\d+)/agenda/(?P<owner>[A-Za-z0-9-.+_]+@[A-Za-z0-9._]+)/(?P<name>[A-Za-z0-9-:_]+)/details$', views.edit_agenda_properties),
    (r'^(?P<num>\d+)/agenda/(?P<owner>[A-Za-z0-9-.+_]+@[A-Za-z0-9._]+)/(?P<name>[A-Za-z0-9-:_]+).(?P<ext>.html)?/?$', views.agenda),
    (r'^(?P<num>\d+)/agenda/(?P<owner>[A-Za-z0-9-.+_]+@[A-Za-z0-9._]+)/(?P<name>[A-Za-z0-9-:_]+)/permissions$', ajax.agenda_permission_api),
    (r'^(?P<num>\d+)/agenda/(?P<owner>[A-Za-z0-9-.+_]+@[A-Za-z0-9._]+)/(?P<name>[A-Za-z0-9-:_]+)/session/(?P<scheduledsession_id>\d+).json$',                                           ajax.scheduledsession_json),
    (r'^(?P<num>\d+)/agenda/(?P<owner>[A-Za-z0-9-.+_]+@[A-Za-z0-9._]+)/(?P<name>[A-Za-z0-9-:_]+)/sessions.json$',      ajax.scheduledsessions_json),
    (r'^(?P<num>\d+)/agenda/(?P<owner>[A-Za-z0-9-.+_]+@[A-Za-z0-9._]+)/(?P<name>[A-Za-z0-9-:_]+).json$', ajax.agenda_infourl),
    (r'^(?P<num>\d+)/agenda/edit$', views.edit_agenda),
    (r'^(?P<num>\d+)/agenda(-utc)?(?P<ext>.html)?/?$',     views.agenda),
    (r'^(?P<num>\d+)/requests.html$', RedirectView.as_view(url='/meeting/%(num)s/requests', permanent=True)),
    (r'^(?P<num>\d+)/requests$', views.meeting_requests),
    (r'^(?P<num>\d+)/agenda(?P<ext>.txt)$', views.agenda),
    (r'^(?P<num>\d+)/agenda.ics$', views.ical_agenda),
    (r'^(?P<num>\d+)/agenda(?P<ext>.csv)$', views.agenda),
    (r'^(?P<num>\d+)/agendas/edit$',                       views.edit_agendas),
    (r'^(?P<num>\d+)/timeslots/edit$',                     views.edit_timeslots),
    (r'^(?P<num>\d+)/rooms$',                              ajax.timeslot_roomsurl),
    (r'^(?P<num>\d+)/room/(?P<roomid>\d+).json$',          ajax.timeslot_roomurl),
    (r'^(?P<num>\d+)/room/(?P<roomid>\d+).html$',          views.edit_roomurl),
    (r'^(?P<num>\d+)/timeslots$',                          ajax.timeslot_slotsurl),
    (r'^(?P<num>\d+)/timeslots.json$',                     ajax.timeslot_slotsurl),
    (r'^(?P<num>\d+)/timeslot/(?P<slotid>\d+).json$',      ajax.timeslot_sloturl),
    (r'^(?P<num>\d+)/agendas$',                            ajax.agenda_infosurl),
    (r'^(?P<num>\d+)/agendas.json$',                       ajax.agenda_infosurl),
    (r'^(?P<num>\d+)/week-view.html$', views.week_view),
    (r'^(?P<num>\d+)/agenda/week-view.html$', views.week_view),
    (r'^(?P<num>\d+)/agenda/(?P<session>[A-Za-z0-9-]+)-drafts.pdf$', views.session_draft_pdf),
    (r'^(?P<num>\d+)/agenda/(?P<session>[A-Za-z0-9-]+)-drafts.tgz$', views.session_draft_tarfile),
    (r'^(?P<num>\d+)/agenda/(?P<session>[A-Za-z0-9-]+)/?$', views.session_agenda),
    (r'^(?P<num>\d+)/sessions.json',                               ajax.sessions_json),
    (r'^(?P<num>\d+)/session/(?P<sessionid>\d+).json',             ajax.session_json),
    (r'^(?P<num>\d+)/session/(?P<sessionid>\d+)/constraints.json', ajax.session_constraints),

    (r'^(?P<num>\d+)/session/(?P<acronym>[A-Za-z0-9_\-\+]+)/$',  views.session_details),
    (r'^(?P<num>\d+)/session/(?P<acronym>[A-Za-z0-9_\-\+]+)/(?P<seq>\d+)/$',  views.session_details),
    (r'^(?P<num>\d+)/session/(?P<acronym>[A-Za-z0-9_\-\+]+)/(?P<week_day>[a-zA-Z]+)/$',  views.session_details),
    (r'^(?P<num>\d+)/session/(?P<acronym>[A-Za-z0-9_\-\+]+)/(?P<date>\d{4}-\d{2}-\d{2}(-\d{4})?)/$',  views.session_details),
    (r'^(?P<num>\d+)/session/(?P<acronym>[A-Za-z0-9_\-\+]+)/(?P<date>\d{4}-\d{2}-\d{2}(-\d{4})?)/(?P<seq>\d+)/$',  views.session_details),

    (r'^(?P<num>\d+)/constraint/(?P<constraintid>\d+).json',       ajax.constraint_json),
    (r'^(?P<num>\d+).json$',                               ajax.meeting_json),
    (r'^$', views.current_materials),
)


