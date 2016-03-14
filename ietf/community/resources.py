# Autogenerated by the mkresources management command 2014-11-13 23:53
from tastypie.resources import ModelResource
from tastypie.fields import ToOneField, ToManyField
from tastypie.constants import ALL, ALL_WITH_RELATIONS

from ietf import api

from ietf.community.models import *     # pyflakes:ignore


from ietf.doc.resources import DocumentResource
from ietf.group.resources import GroupResource
from ietf.utils.resources import UserResource
class CommunityListResource(ModelResource):
    user             = ToOneField(UserResource, 'user', null=True)
    group            = ToOneField(GroupResource, 'group', null=True)
    added_docs       = ToManyField(DocumentResource, 'added_docs', null=True)
    class Meta:
        queryset = CommunityList.objects.all()
        serializer = api.Serializer()
        #resource_name = 'communitylist'
        filtering = { 
            "id": ALL,
            "secret": ALL,
            "cached": ALL,
            "user": ALL_WITH_RELATIONS,
            "group": ALL_WITH_RELATIONS,
            "added_docs": ALL_WITH_RELATIONS,
        }
api.community.register(CommunityListResource())

from ietf.doc.resources import DocumentResource
class SearchRuleResource(ModelResource):
    community_list   = ToOneField(CommunityListResource, 'community_list')
    class Meta:
        queryset = SearchRule.objects.all()
        serializer = api.Serializer()
        #resource_name = 'rule'
        filtering = { 
            "id": ALL,
            "rule_type": ALL,
            "community_list": ALL_WITH_RELATIONS,
        }
api.community.register(SearchRuleResource())

class EmailSubscriptionResource(ModelResource):
    community_list   = ToOneField(CommunityListResource, 'community_list')
    class Meta:
        queryset = EmailSubscription.objects.all()
        serializer = api.Serializer()
        #resource_name = 'emailsubscription'
        filtering = { 
            "id": ALL,
            "email": ALL,
            "significant": ALL,
            "community_list": ALL_WITH_RELATIONS,
        }
api.community.register(EmailSubscriptionResource())
