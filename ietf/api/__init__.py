# Copyright The IETF Trust 2014-2019, All Rights Reserved
# -*- coding: utf-8 -*-


from __future__ import absolute_import, print_function, unicode_literals

import datetime
import re
import six

from six.moves.urllib.parse import urlencode

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

import debug                            # pyflakes:ignore

import tastypie
import tastypie.resources
from tastypie.api import Api
from tastypie.bundle import Bundle
from tastypie.exceptions import ApiFieldError
from tastypie.serializers import Serializer # pyflakes:ignore (we're re-exporting this)
from tastypie.fields import ApiField

_api_list = []

for _app in settings.INSTALLED_APPS:
    _module_dict = globals()
    if '.' in _app:
        _root, _name = _app.split('.', 1)
        if _root == 'ietf':
            if not '.' in _name:
                _api = Api(api_name=_name)
                _module_dict[_name] = _api
                _api_list.append((_name, _api))

def autodiscover():
    """
    Auto-discover INSTALLED_APPS resources.py modules and fail silently when
    not present. This forces an import on them to register any admin bits they
    may want.
    """

    from importlib import import_module
    from django.conf import settings
    from django.utils.module_loading import module_has_submodule

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        # Attempt to import the app's admin module.
        try:
            import_module('%s.resources' % (app, ))
        except:
            # Decide whether to bubble up this error. If the app just
            # doesn't have an admin module, we can ignore the error
            # attempting to import it, otherwise we want it to bubble up.
            if module_has_submodule(mod, "resources"):
                raise

class ModelResource(tastypie.resources.ModelResource):
    def generate_cache_key(self, *args, **kwargs):
        """
        Creates a unique-enough cache key.

        This is based off the current api_name/resource_name/args/kwargs.
        """
        #smooshed = ["%s=%s" % (key, value) for key, value in kwargs.items()]
        smooshed = urlencode(kwargs)

        # Use a list plus a ``.join()`` because it's faster than concatenation.
        return "%s:%s:%s:%s" % (self._meta.api_name, self._meta.resource_name, ':'.join(args), smooshed)


TIMEDELTA_REGEX = re.compile(r'^(?P<days>\d+d)?\s?(?P<hours>\d+h)?\s?(?P<minutes>\d+m)?\s?(?P<seconds>\d+s?)$')

class TimedeltaField(ApiField):
    dehydrated_type = 'timedelta'
    help_text = "A timedelta field, with duration expressed in seconds. Ex: 132"

    def convert(self, value):
        if value is None:
            return None

        if isinstance(value, six.string_types):
            match = TIMEDELTA_REGEX.search(value)

            if match:
                data = match.groupdict()
                return datetime.timedelta(int(data['days']), int(data['hours']), int(data['minutes']), int(data['seconds']))
            else:
                raise ApiFieldError("Timedelta provided to '%s' field doesn't appear to be a valid timedelta string: '%s'" % (self.instance_name, value))

        return value

    def hydrate(self, bundle):
        value = super(TimedeltaField, self).hydrate(bundle)

        if value and not hasattr(value, 'seconds'):
            if isinstance(value, six.string_types):
                try:
                    match = TIMEDELTA_REGEX.search(value)

                    if match:
                        data = match.groupdict()
                        value = datetime.timedelta(int(data['days']), int(data['hours']), int(data['minutes']), int(data['seconds']))
                    else:
                        raise ValueError()
                except (ValueError, TypeError):
                    raise ApiFieldError("Timedelta provided to '%s' field doesn't appear to be a valid datetime string: '%s'" % (self.instance_name, value))

            else:
                raise ApiFieldError("Datetime provided to '%s' field must be a string: %s" % (self.instance_name, value))

        return value

class ToOneField(tastypie.fields.ToOneField):
    "Subclass of tastypie.fields.ToOneField which adds caching in the dehydrate method."

    def dehydrate(self, bundle, for_list=True):
        foreign_obj = None
        previous_obj = None
        attrib = None
        
        if callable(self.attribute):
            previous_obj = bundle.obj
            foreign_obj = self.attribute(bundle)
        elif isinstance(self.attribute, six.string_types):
            foreign_obj = bundle.obj

            for attr in self._attrs:
                attrib = attr
                previous_obj = foreign_obj
                try:
                    foreign_obj = getattr(foreign_obj, attr, None)
                except ObjectDoesNotExist:
                    foreign_obj = None

        if not foreign_obj:
            if not self.null:
                if callable(self.attribute):
                    raise ApiFieldError("The related resource for resource %s could not be found." % (previous_obj))
                else:
                    raise ApiFieldError("The model '%r' has an empty attribute '%s' and doesn't allow a null value." % (previous_obj, attrib))
            return None

        fk_resource = self.get_related_resource(foreign_obj)

        # Up to this point we've copied the code from tastypie 0.13.1.  Now
        # we add caching.
        cache_key = fk_resource.generate_cache_key('related', pk=foreign_obj.pk, for_list=for_list, )
        dehydrated = fk_resource._meta.cache.get(cache_key)
        if dehydrated is None:
            fk_bundle = Bundle(obj=foreign_obj, request=bundle.request)
            dehydrated = self.dehydrate_related(fk_bundle, fk_resource, for_list=for_list)
            fk_resource._meta.cache.set(cache_key, dehydrated)
        return dehydrated
