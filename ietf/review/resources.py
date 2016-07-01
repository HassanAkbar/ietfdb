# Autogenerated by the makeresources management command 2016-06-14 04:21 PDT
from tastypie.resources import ModelResource
from tastypie.fields import ToManyField                 # pyflakes:ignore
from tastypie.constants import ALL, ALL_WITH_RELATIONS  # pyflakes:ignore
from tastypie.cache import SimpleCache

from ietf import api
from ietf.api import ToOneField                         # pyflakes:ignore

from ietf.review.models import Reviewer, ReviewRequest, ReviewTeamResult


from ietf.person.resources import PersonResource
from ietf.group.resources import GroupResource
class ReviewerResource(ModelResource):
    team             = ToOneField(GroupResource, 'team')
    person           = ToOneField(PersonResource, 'person')
    class Meta:
        queryset = Reviewer.objects.all()
        serializer = api.Serializer()
        cache = SimpleCache()
        #resource_name = 'reviewer'
        filtering = { 
            "id": ALL,
            "frequency": ALL,
            "unavailable_until": ALL,
            "filter_re": ALL,
            "skip_next": ALL,
            "team": ALL_WITH_RELATIONS,
            "person": ALL_WITH_RELATIONS,
        }
api.review.register(ReviewerResource())

from ietf.doc.resources import DocumentResource
from ietf.group.resources import RoleResource, GroupResource
from ietf.name.resources import ReviewRequestStateNameResource, ReviewResultNameResource, ReviewTypeNameResource
class ReviewRequestResource(ModelResource):
    state            = ToOneField(ReviewRequestStateNameResource, 'state')
    type             = ToOneField(ReviewTypeNameResource, 'type')
    doc              = ToOneField(DocumentResource, 'doc')
    team             = ToOneField(GroupResource, 'team')
    reviewer         = ToOneField(RoleResource, 'reviewer', null=True)
    review           = ToOneField(DocumentResource, 'review', null=True)
    result           = ToOneField(ReviewResultNameResource, 'result', null=True)
    class Meta:
        queryset = ReviewRequest.objects.all()
        serializer = api.Serializer()
        cache = SimpleCache()
        #resource_name = 'reviewrequest'
        filtering = { 
            "id": ALL,
            "time": ALL,
            "deadline": ALL,
            "requested_rev": ALL,
            "reviewed_rev": ALL,
            "state": ALL_WITH_RELATIONS,
            "type": ALL_WITH_RELATIONS,
            "doc": ALL_WITH_RELATIONS,
            "team": ALL_WITH_RELATIONS,
            "reviewer": ALL_WITH_RELATIONS,
            "review": ALL_WITH_RELATIONS,
            "result": ALL_WITH_RELATIONS,
        }
api.review.register(ReviewRequestResource())



from ietf.group.resources import GroupResource
from ietf.name.resources import ReviewResultNameResource
class ReviewTeamResultResource(ModelResource):
    team             = ToOneField(GroupResource, 'team')
    result           = ToOneField(ReviewResultNameResource, 'result')
    class Meta:
        queryset = ReviewTeamResult.objects.all()
        serializer = api.Serializer()
        cache = SimpleCache()
        #resource_name = 'reviewteamresult'
        filtering = { 
            "id": ALL,
            "team": ALL_WITH_RELATIONS,
            "result": ALL_WITH_RELATIONS,
        }
api.review.register(ReviewTeamResultResource())

