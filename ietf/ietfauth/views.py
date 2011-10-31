# Portions Copyright (C) 2009 Nokia Corporation and/or its subsidiary(-ies).
# All rights reserved. Contact: Pasi Eronen <pasi.eronen@nokia.com>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#
#  * Neither the name of the Nokia Corporation and/or its
#    subsidiary(-ies) nor the names of its contributors may be used
#    to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Copyright The IETF Trust 2007, All Rights Reserved

import datetime
import hashlib

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.utils.http import urlquote

from ietf.ietfauth.forms import (RegistrationForm, PasswordForm,
                                 RecoverPasswordForm)


def index(request):
    return render_to_response('registration/index.html', context_instance=RequestContext(request))


def url_login(request, user, passwd):
    user = authenticate(username=user, password=passwd)
    redirect_to = request.REQUEST.get(REDIRECT_FIELD_NAME, '')
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/accounts/loggedin/?%s=%s' % (REDIRECT_FIELD_NAME, urlquote(redirect_to)))
    return HttpResponse("Not authenticated?", status=500)


def ietf_login(request):
    if not request.user.is_authenticated():
        # This probably means an exception occured inside IetfUserBackend
        return HttpResponse("Not authenticated?", status=500)
    redirect_to = request.REQUEST.get(REDIRECT_FIELD_NAME, '')
    request.session.set_test_cookie()
    return HttpResponseRedirect('/accounts/loggedin/?%s=%s' % (REDIRECT_FIELD_NAME, urlquote(redirect_to)))


def ietf_loggedin(request):
    if not request.session.test_cookie_worked():
        return HttpResponse("You need to enable cookies")
    request.session.delete_test_cookie()
    redirect_to = request.REQUEST.get(REDIRECT_FIELD_NAME, '')
    if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
        redirect_to = settings.LOGIN_REDIRECT_URL
    return HttpResponseRedirect(redirect_to)


@login_required
def profile(request):
    if settings.USE_DB_REDESIGN_PROXY_CLASSES:
        from person.models import Person
        from group.models import Role

        roles = []
        person = None
        try:
            person = request.user.get_profile()
            roles = Role.objects.filter(email__person=person).distinct()
        except Person.DoesNotExist:
            pass

        return render_to_response('registration/profileREDESIGN.html',
                                  dict(roles=roles,
                                       person=person),
                                  context_instance=RequestContext(request))

    return render_to_response('registration/profile.html', context_instance=RequestContext(request))


def create_account(request):
    success = False
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
    else:
        form = RegistrationForm()
    return render_to_response('registration/create.html',
                              {'form': form,
                               'success': success},
                              context_instance=RequestContext(request))


def confirm_account(request, username, date, realm, registration_hash):
    valid = hashlib.md5('%s%s%s%s' % (settings.SECRET_KEY, date, username, realm)).hexdigest() == registration_hash
    if not valid:
        raise Http404
    request_date = datetime.date(int(date[:4]), int(date[4:6]), int(date[6:]))
    if datetime.date.today() > (request_date + datetime.timedelta(days=settings.DAYS_TO_EXPIRE_REGISTRATION_LINK)):
        raise Http404
    success = False
    if request.method == 'POST':
        form = PasswordForm(request.POST, username=username)
        if form.is_valid():
            form.save()
            success = True
    else:
        form = PasswordForm(username=username)
    return render_to_response('registration/confirm.html',
                              {'form': form, 'email': username, 'success': success},
                              context_instance=RequestContext(request))


def password_reset_view(request):
    success = False
    if request.method == 'POST':
        form = RecoverPasswordForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
    else:
        form = RecoverPasswordForm()
    return render_to_response('registration/password_reset.html',
                              {'form': form,
                               'success': success},
                              context_instance=RequestContext(request))


def confirm_password_reset(request, username, date, realm, reset_hash):
    valid = hashlib.md5('%s%s%s%s' % (settings.SECRET_KEY, date, username, realm)).hexdigest() == reset_hash
    if not valid:
        raise Http404
    success = False
    if request.method == 'POST':
        form = PasswordForm(request.POST, update_user=True, username=username)
        if form.is_valid():
            form.save()
            success = True
    else:
        form = PasswordForm(username=username)
    return render_to_response('registration/change_password.html',
                              {'form': form,
                               'success': success,
                               'username': username},
                              context_instance=RequestContext(request))


def ajax_check_username(request):
    username = request.GET.get('username', '')
    error = False
    if User.objects.filter(username=username).count():
        error = 'This email is already in use'
    return HttpResponse(simplejson.dumps({'error': error}), mimetype='text/plain')
