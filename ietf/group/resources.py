# Copyright The IETF Trust 2014-2019, All Rights Reserved
# Autogenerated by the mkresources management command 2014-11-13 23:15
from ietf.api import ModelResource
from ietf.api import ToOneField
from tastypie.fields import ToManyField, CharField
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.cache import SimpleCache

from ietf import api

from ietf.group.models import (Group, GroupStateTransitions, GroupMilestone, GroupHistory,
    GroupURL, Role, GroupEvent, RoleHistory, GroupMilestoneHistory, MilestoneGroupEvent,
    ChangeStateGroupEvent, GroupFeatures, HistoricalGroupFeatures)


from ietf.person.resources import PersonResource
from ietf.name.resources import GroupStateNameResource, GroupTypeNameResource, DocTagNameResource
class GroupResource(ModelResource):
    state = ToOneField(GroupStateNameResource, 'state', null=True)
    type = ToOneField(GroupTypeNameResource, 'type', null=True)
    parent = ToOneField('ietf.group.resources.GroupResource', 'parent', null=True)
    ad = ToOneField(PersonResource, 'ad', null=True)
    charter = ToOneField('ietf.doc.resources.DocumentResource', 'charter', null=True)
    unused_states = ToManyField('ietf.doc.resources.StateResource', 'unused_states', null=True)
    unused_tags = ToManyField(DocTagNameResource, 'unused_tags', null=True)
    description = CharField(attribute='get_description')
    class Meta:
        cache = SimpleCache()
        queryset = Group.objects.all()
        serializer = api.Serializer()
        #resource_name = 'group'
        ordering = ['id', ]
        filtering = { 
            "id": ALL,
            "time": ALL,
            "name": ALL,
            "description": ALL,
            "list_email": ALL,
            "list_subscribe": ALL,
            "list_archive": ALL,
            "comments": ALL,
            "acronym": ALL,
            "state": ALL_WITH_RELATIONS,
            "type": ALL_WITH_RELATIONS,
            "parent": ALL_WITH_RELATIONS,
            "ad": ALL_WITH_RELATIONS,
            "charter": ALL_WITH_RELATIONS,
            "unused_states": ALL_WITH_RELATIONS,
            "unused_tags": ALL_WITH_RELATIONS,
        }
api.group.register(GroupResource())

class GroupStateTransitionsResource(ModelResource):
    group = ToOneField(GroupResource, 'group')
    state = ToOneField('ietf.doc.resources.StateResource', 'state')
    next_states = ToManyField('ietf.doc.resources.StateResource', 'next_states', null=True)
    class Meta:
        cache = SimpleCache()
        queryset = GroupStateTransitions.objects.all()
        serializer = api.Serializer()
        #resource_name = 'groupstatetransitions'
        ordering = ['id', ]
        filtering = { 
            "id": ALL,
            "group": ALL_WITH_RELATIONS,
            "state": ALL_WITH_RELATIONS,
            "next_states": ALL_WITH_RELATIONS,
        }
api.group.register(GroupStateTransitionsResource())

from ietf.name.resources import GroupMilestoneStateNameResource
class GroupMilestoneResource(ModelResource):
    group = ToOneField(GroupResource, 'group')
    state = ToOneField(GroupMilestoneStateNameResource, 'state')
    docs = ToManyField('ietf.doc.resources.DocumentResource', 'docs', null=True)
    class Meta:
        cache = SimpleCache()
        queryset = GroupMilestone.objects.all()
        serializer = api.Serializer()
        #resource_name = 'groupmilestone'
        ordering = ['id', ]
        filtering = { 
            "id": ALL,
            "desc": ALL,
            "due": ALL,
            "resolved": ALL,
            "time": ALL,
            "group": ALL_WITH_RELATIONS,
            "state": ALL_WITH_RELATIONS,
            "docs": ALL_WITH_RELATIONS,
        }
api.group.register(GroupMilestoneResource())

from ietf.person.resources import PersonResource
from ietf.name.resources import GroupStateNameResource, GroupTypeNameResource, DocTagNameResource
class GroupHistoryResource(ModelResource):
    state = ToOneField(GroupStateNameResource, 'state', null=True)
    type = ToOneField(GroupTypeNameResource, 'type', null=True)
    parent = ToOneField(GroupResource, 'parent', null=True)
    ad = ToOneField(PersonResource, 'ad', null=True)
    group = ToOneField(GroupResource, 'group')
    unused_states = ToManyField('ietf.doc.resources.StateResource', 'unused_states', null=True)
    unused_tags = ToManyField(DocTagNameResource, 'unused_tags', null=True)
    class Meta:
        cache = SimpleCache()
        queryset = GroupHistory.objects.all()
        serializer = api.Serializer()
        #resource_name = 'grouphistory'
        ordering = ['id', ]
        filtering = { 
            "id": ALL,
            "time": ALL,
            "name": ALL,
            "description": ALL,
            "list_email": ALL,
            "list_subscribe": ALL,
            "list_archive": ALL,
            "comments": ALL,
            "acronym": ALL,
            "state": ALL_WITH_RELATIONS,
            "type": ALL_WITH_RELATIONS,
            "parent": ALL_WITH_RELATIONS,
            "ad": ALL_WITH_RELATIONS,
            "group": ALL_WITH_RELATIONS,
            "unused_states": ALL_WITH_RELATIONS,
            "unused_tags": ALL_WITH_RELATIONS,
        }
api.group.register(GroupHistoryResource())

class GroupURLResource(ModelResource):
    group = ToOneField(GroupResource, 'group')
    class Meta:
        cache = SimpleCache()
        queryset = GroupURL.objects.all()
        serializer = api.Serializer()
        #resource_name = 'groupurl'
        ordering = ['id', ]
        filtering = { 
            "id": ALL,
            "name": ALL,
            "url": ALL,
            "group": ALL_WITH_RELATIONS,
        }
api.group.register(GroupURLResource())

from ietf.person.resources import PersonResource, EmailResource
from ietf.name.resources import RoleNameResource
class RoleResource(ModelResource):
    name = ToOneField(RoleNameResource, 'name')
    group = ToOneField(GroupResource, 'group')
    person = ToOneField(PersonResource, 'person')
    email = ToOneField(EmailResource, 'email')
    class Meta:
        cache = SimpleCache()
        queryset = Role.objects.all()
        serializer = api.Serializer()
        #resource_name = 'role'
        ordering = ['id', ]
        filtering = { 
            "id": ALL,
            "name": ALL_WITH_RELATIONS,
            "group": ALL_WITH_RELATIONS,
            "person": ALL_WITH_RELATIONS,
            "email": ALL_WITH_RELATIONS,
        }
api.group.register(RoleResource())

from ietf.person.resources import PersonResource
class GroupEventResource(ModelResource):
    group = ToOneField(GroupResource, 'group')
    by = ToOneField(PersonResource, 'by')
    class Meta:
        cache = SimpleCache()
        queryset = GroupEvent.objects.all()
        serializer = api.Serializer()
        #resource_name = 'groupevent'
        ordering = ['id', ]
        filtering = { 
            "id": ALL,
            "time": ALL,
            "type": ALL,
            "desc": ALL,
            "group": ALL_WITH_RELATIONS,
            "by": ALL_WITH_RELATIONS,
        }
api.group.register(GroupEventResource())

from ietf.person.resources import PersonResource, EmailResource
from ietf.name.resources import RoleNameResource
class RoleHistoryResource(ModelResource):
    name = ToOneField(RoleNameResource, 'name')
    group = ToOneField(GroupHistoryResource, 'group')
    person = ToOneField(PersonResource, 'person')
    email = ToOneField(EmailResource, 'email')
    class Meta:
        cache = SimpleCache()
        queryset = RoleHistory.objects.all()
        serializer = api.Serializer()
        #resource_name = 'rolehistory'
        ordering = ['id', ]
        filtering = { 
            "id": ALL,
            "name": ALL_WITH_RELATIONS,
            "group": ALL_WITH_RELATIONS,
            "person": ALL_WITH_RELATIONS,
            "email": ALL_WITH_RELATIONS,
        }
api.group.register(RoleHistoryResource())

from ietf.name.resources import GroupMilestoneStateNameResource
class GroupMilestoneHistoryResource(ModelResource):
    group = ToOneField(GroupResource, 'group')
    state = ToOneField(GroupMilestoneStateNameResource, 'state')
    milestone = ToOneField(GroupMilestoneResource, 'milestone')
    docs = ToManyField('ietf.doc.resources.DocumentResource', 'docs', null=True)
    class Meta:
        cache = SimpleCache()
        queryset = GroupMilestoneHistory.objects.all()
        serializer = api.Serializer()
        #resource_name = 'groupmilestonehistory'
        ordering = ['id', ]
        filtering = { 
            "id": ALL,
            "desc": ALL,
            "due": ALL,
            "resolved": ALL,
            "time": ALL,
            "group": ALL_WITH_RELATIONS,
            "state": ALL_WITH_RELATIONS,
            "milestone": ALL_WITH_RELATIONS,
            "docs": ALL_WITH_RELATIONS,
        }
api.group.register(GroupMilestoneHistoryResource())

from ietf.person.resources import PersonResource
class MilestoneGroupEventResource(ModelResource):
    group = ToOneField(GroupResource, 'group')
    by = ToOneField(PersonResource, 'by')
    groupevent_ptr = ToOneField(GroupEventResource, 'groupevent_ptr')
    milestone = ToOneField(GroupMilestoneResource, 'milestone')
    class Meta:
        cache = SimpleCache()
        queryset = MilestoneGroupEvent.objects.all()
        serializer = api.Serializer()
        #resource_name = 'milestonegroupevent'
        ordering = ['id', ]
        filtering = { 
            "id": ALL,
            "time": ALL,
            "type": ALL,
            "desc": ALL,
            "group": ALL_WITH_RELATIONS,
            "by": ALL_WITH_RELATIONS,
            "groupevent_ptr": ALL_WITH_RELATIONS,
            "milestone": ALL_WITH_RELATIONS,
        }
api.group.register(MilestoneGroupEventResource())

from ietf.person.resources import PersonResource
from ietf.name.resources import GroupStateNameResource
class ChangeStateGroupEventResource(ModelResource):
    group = ToOneField(GroupResource, 'group')
    by = ToOneField(PersonResource, 'by')
    groupevent_ptr = ToOneField(GroupEventResource, 'groupevent_ptr')
    state = ToOneField(GroupStateNameResource, 'state')
    class Meta:
        cache = SimpleCache()
        queryset = ChangeStateGroupEvent.objects.all()
        serializer = api.Serializer()
        #resource_name = 'changestategroupevent'
        ordering = ['id', ]
        filtering = { 
            "id": ALL,
            "time": ALL,
            "type": ALL,
            "desc": ALL,
            "group": ALL_WITH_RELATIONS,
            "by": ALL_WITH_RELATIONS,
            "groupevent_ptr": ALL_WITH_RELATIONS,
            "state": ALL_WITH_RELATIONS,
        }
api.group.register(ChangeStateGroupEventResource())

from ietf.name.resources import GroupTypeNameResource, AgendaTypeNameResource
class GroupFeaturesResource(ModelResource):
    type             = ToOneField(GroupTypeNameResource, 'type')
    agenda_type      = ToOneField(AgendaTypeNameResource, 'agenda_type', null=True)
    class Meta:
        queryset = GroupFeatures.objects.all()
        serializer = api.Serializer()
        cache = SimpleCache()
        #resource_name = 'groupfeatures'
        ordering = ['id', ]
        filtering = { 
            "has_milestones": ALL,
            "has_chartering_process": ALL,
            "has_documents": ALL,
            "has_dependencies": ALL,
            "has_nonsession_materials": ALL,
            "has_meetings": ALL,
            "has_reviews": ALL,
            "has_default_jabber": ALL,
            "customize_workflow": ALL,
            "about_page": ALL,
            "default_tab": ALL,
            "material_types": ALL,
            "admin_roles": ALL,
            "type": ALL_WITH_RELATIONS,
            "agenda_type": ALL_WITH_RELATIONS,
        }
api.group.register(GroupFeaturesResource())

from ietf.name.resources import GroupTypeNameResource, AgendaTypeNameResource
from ietf.utils.resources import UserResource
class HistoricalGroupFeaturesResource(ModelResource):
    type             = ToOneField(GroupTypeNameResource, 'type', null=True)
    agenda_type      = ToOneField(AgendaTypeNameResource, 'agenda_type', null=True)
    history_user     = ToOneField(UserResource, 'history_user', null=True)
    class Meta:
        queryset = HistoricalGroupFeatures.objects.all()
        serializer = api.Serializer()
        cache = SimpleCache()
        #resource_name = 'historicalgroupfeatures'
        ordering = ['id', ]
        filtering = { 
            "has_milestones": ALL,
            "has_chartering_process": ALL,
            "has_documents": ALL,
            "has_dependencies": ALL,
            "has_nonsession_materials": ALL,
            "has_meetings": ALL,
            "has_reviews": ALL,
            "has_default_jabber": ALL,
            "customize_workflow": ALL,
            "about_page": ALL,
            "default_tab": ALL,
            "material_types": ALL,
            "admin_roles": ALL,
            "history_id": ALL,
            "history_change_reason": ALL,
            "history_date": ALL,
            "history_type": ALL,
            "type": ALL_WITH_RELATIONS,
            "agenda_type": ALL_WITH_RELATIONS,
            "history_user": ALL_WITH_RELATIONS,
        }
api.group.register(HistoricalGroupFeaturesResource())
