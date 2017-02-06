# Autogenerated by the mkresources management command 2014-11-13 23:53
from ietf.api import ModelResource
from tastypie.fields import ToOneField
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.cache import SimpleCache

from ietf import api

from ietf.person.models import (Person, Email, Alias, PersonHistory,
    AffiliationAlias, AffiliationIgnoredEnding)


from ietf.utils.resources import UserResource
class PersonResource(ModelResource):
    user             = ToOneField(UserResource, 'user', null=True)
    class Meta:
        cache = SimpleCache()
        queryset = Person.objects.all()
        serializer = api.Serializer()
        #resource_name = 'person'
        filtering = { 
            "id": ALL,
            "time": ALL,
            "name": ALL,
            "ascii": ALL,
            "ascii_short": ALL,
            "address": ALL,
            "affiliation": ALL,
            "photo": ALL,
            "biography": ALL,
            "user": ALL_WITH_RELATIONS,
        }
api.person.register(PersonResource())

class EmailResource(ModelResource):
    person           = ToOneField(PersonResource, 'person', null=True)
    class Meta:
        cache = SimpleCache()
        queryset = Email.objects.all()
        serializer = api.Serializer()
        #resource_name = 'email'
        filtering = { 
            "address": ALL,
            "time": ALL,
            "active": ALL,
            "person": ALL_WITH_RELATIONS,
        }
api.person.register(EmailResource())

class AliasResource(ModelResource):
    person           = ToOneField(PersonResource, 'person')
    class Meta:
        cache = SimpleCache()
        queryset = Alias.objects.all()
        serializer = api.Serializer()
        #resource_name = 'alias'
        filtering = { 
            "id": ALL,
            "name": ALL,
            "person": ALL_WITH_RELATIONS,
        }
api.person.register(AliasResource())

from ietf.utils.resources import UserResource
class PersonHistoryResource(ModelResource):
    person           = ToOneField(PersonResource, 'person')
    user             = ToOneField(UserResource, 'user', null=True)
    class Meta:
        cache = SimpleCache()
        queryset = PersonHistory.objects.all()
        serializer = api.Serializer()
        #resource_name = 'personhistory'
        filtering = { 
            "id": ALL,
            "time": ALL,
            "name": ALL,
            "ascii": ALL,
            "ascii_short": ALL,
            "address": ALL,
            "affiliation": ALL,
            "person": ALL_WITH_RELATIONS,
            "user": ALL_WITH_RELATIONS,
        }
api.person.register(PersonHistoryResource())

class AffiliationIgnoredEndingResource(ModelResource):
    class Meta:
        queryset = AffiliationIgnoredEnding.objects.all()
        serializer = api.Serializer()
        cache = SimpleCache()
        #resource_name = 'affiliationignoredending'
        filtering = { 
            "id": ALL,
            "ending": ALL,
        }
api.person.register(AffiliationIgnoredEndingResource())

class AffiliationAliasResource(ModelResource):
    class Meta:
        queryset = AffiliationAlias.objects.all()
        serializer = api.Serializer()
        cache = SimpleCache()
        #resource_name = 'affiliationalias'
        filtering = { 
            "id": ALL,
            "alias": ALL,
            "name": ALL,
        }
api.person.register(AffiliationAliasResource())

