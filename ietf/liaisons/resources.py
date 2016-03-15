# Autogenerated by the makeresources management command 2015-10-11 13:15 PDT
from tastypie.resources import ModelResource
from ietf.api import ToOneField
from tastypie.field import ToManyField     # pyflakes:ignore
from tastypie.constants import ALL, ALL_WITH_RELATIONS  # pyflakes:ignore
from tastypie.cache import SimpleCache

from ietf import api

from ietf.liaisons.models import (LiaisonStatement, LiaisonStatementGroupContacts,
    LiaisonStatementEvent, LiaisonStatementAttachment, RelatedLiaisonStatement)


from ietf.person.resources import EmailResource
from ietf.group.resources import GroupResource
from ietf.name.resources import LiaisonStatementPurposeNameResource, LiaisonStatementTagNameResource, LiaisonStatementStateResource
from ietf.doc.resources import DocumentResource
class LiaisonStatementResource(ModelResource):
    from_contact     = ToOneField(EmailResource, 'from_contact', null=True)
    purpose          = ToOneField(LiaisonStatementPurposeNameResource, 'purpose')
    state            = ToOneField(LiaisonStatementStateResource, 'state')
    from_groups      = ToManyField(GroupResource, 'from_groups', null=True)
    to_groups        = ToManyField(GroupResource, 'to_groups', null=True)
    tags             = ToManyField(LiaisonStatementTagNameResource, 'tags', null=True)
    attachments      = ToManyField(DocumentResource, 'attachments', null=True)
    class Meta:
        cache = SimpleCache()
        queryset = LiaisonStatement.objects.all()
        serializer = api.Serializer()
        #resource_name = 'liaisonstatement'
        filtering = { 
            "id": ALL,
            "title": ALL,
            "to_contacts": ALL,
            "response_contacts": ALL,
            "technical_contacts": ALL,
            "action_holder_contacts": ALL,
            "cc_contacts": ALL,
            "deadline": ALL,
            "other_identifiers": ALL,
            "body": ALL,
            "from_name": ALL,
            "to_name": ALL,
            "from_contact": ALL_WITH_RELATIONS,
            "purpose": ALL_WITH_RELATIONS,
            "state": ALL_WITH_RELATIONS,
            "from_groups": ALL_WITH_RELATIONS,
            "to_groups": ALL_WITH_RELATIONS,
            "tags": ALL_WITH_RELATIONS,
            "attachments": ALL_WITH_RELATIONS,
        }
api.liaisons.register(LiaisonStatementResource())

from ietf.group.resources import GroupResource
class LiaisonStatementGroupContactsResource(ModelResource):
    group            = ToOneField(GroupResource, 'group')
    class Meta:
        cache = SimpleCache()
        queryset = LiaisonStatementGroupContacts.objects.all()
        serializer = api.Serializer()
        #resource_name = 'liaisonstatementgroupcontacts'
        filtering = { 
            "id": ALL,
            "contacts": ALL,
            "cc_contacts": ALL,
            "group": ALL_WITH_RELATIONS,
        }
api.liaisons.register(LiaisonStatementGroupContactsResource())

from ietf.person.resources import PersonResource
from ietf.name.resources import LiaisonStatementEventTypeNameResource
class LiaisonStatementEventResource(ModelResource):
    type             = ToOneField(LiaisonStatementEventTypeNameResource, 'type')
    by               = ToOneField(PersonResource, 'by')
    statement        = ToOneField(LiaisonStatementResource, 'statement')
    class Meta:
        cache = SimpleCache()
        queryset = LiaisonStatementEvent.objects.all()
        serializer = api.Serializer()
        #resource_name = 'liaisonstatementevent'
        filtering = { 
            "id": ALL,
            "time": ALL,
            "desc": ALL,
            "type": ALL_WITH_RELATIONS,
            "by": ALL_WITH_RELATIONS,
            "statement": ALL_WITH_RELATIONS,
        }
api.liaisons.register(LiaisonStatementEventResource())

from ietf.doc.resources import DocumentResource
class LiaisonStatementAttachmentResource(ModelResource):
    statement        = ToOneField(LiaisonStatementResource, 'statement')
    document         = ToOneField(DocumentResource, 'document')
    class Meta:
        cache = SimpleCache()
        queryset = LiaisonStatementAttachment.objects.all()
        serializer = api.Serializer()
        #resource_name = 'liaisonstatementattachment'
        filtering = { 
            "id": ALL,
            "removed": ALL,
            "statement": ALL_WITH_RELATIONS,
            "document": ALL_WITH_RELATIONS,
        }
api.liaisons.register(LiaisonStatementAttachmentResource())

from ietf.name.resources import DocRelationshipNameResource
class RelatedLiaisonStatementResource(ModelResource):
    source           = ToOneField(LiaisonStatementResource, 'source')
    target           = ToOneField(LiaisonStatementResource, 'target')
    relationship     = ToOneField(DocRelationshipNameResource, 'relationship')
    class Meta:
        cache = SimpleCache()
        queryset = RelatedLiaisonStatement.objects.all()
        serializer = api.Serializer()
        #resource_name = 'relatedliaisonstatement'
        filtering = { 
            "id": ALL,
            "source": ALL_WITH_RELATIONS,
            "target": ALL_WITH_RELATIONS,
            "relationship": ALL_WITH_RELATIONS,
        }
api.liaisons.register(RelatedLiaisonStatementResource())

