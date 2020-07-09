# Copyright The IETF Trust 2020, All Rights Reserved
# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-03-19 13:06
from __future__ import unicode_literals

import re

import debug

from collections import OrderedDict, Counter

from django.db import migrations

from ietf.utils.validators import validate_external_resource_value
from django.core.exceptions import ValidationError


name_map = {
    "Issue.*":                "tracker",
    ".*FAQ.*":                "faq",
    ".*Area Web Page":        "webpage",
    ".*Wiki":                 "wiki",
    "Home Page":              "webpage",
    "Slack.*":                "slack",
    "Additional .* Web Page": "webpage",
    "Additional .* Page":     "webpage",
    "Yang catalog entry.*":   "yc_entry",
    "Yang impact analysis.*": "yc_impact",
    "GitHub":                 "github_repo",
    "Github page":            "github_repo",
    "GitHub repo.*":          "github_repo",
    "Github repository.*":    "github_repo",
    "GitHub notifications":   "github_notify",
    "GitHub org.*":           "github_org",
    "GitHub User.*":          "github_username",
    "GitLab User":            "gitlab_username",
    "GitLab User Name":       "gitlab_username",
}

# TODO: Review all the None values below and make sure ignoring the URLs they match is really the right thing to do.
url_map = OrderedDict({
   "https?://github\\.com": "github_repo",
   "https://git.sr.ht/": "repo",
   "https://todo.sr.ht/": "tracker",
   "https?://trac\\.ietf\\.org/.*/wiki": "wiki",
   "ietf\\.org.*/trac/wiki": "wiki",
   "trac.*wiki": "wiki",
   "www\\.ietf\\.org/mailman" : None,
   "www\\.ietf\\.org/mail-archive" : None,
   "mailarchive\\.ietf\\.org" : None,
   "ietf\\.org/logs": "jabber_log",
   "ietf\\.org/jabber/logs": "jabber_log",
   "xmpp:.*?join": "jabber_room",
   "bell-labs\\.com": None,
   "html\\.charters": None,
   "datatracker\\.ietf\\.org": None,
})

def forward(apps, schema_editor):
    DocExtResource = apps.get_model('doc', 'DocExtResource')
    ExtResourceName = apps.get_model('name', 'ExtResourceName')
    DocumentUrl = apps.get_model('doc', 'DocumentUrl')

    stats = Counter()

    for doc_url in DocumentUrl.objects.all():
        match_found = False
        for regext,slug in name_map.items():
            if re.match(regext, doc_url.desc):
                match_found = True
                stats['mapped'] += 1
                name = ExtResourceName.objects.get(slug=slug)
                DocExtResource.objects.create(doc=doc_url.doc, name_id=slug, value=doc_url.url, display_name=doc_url.desc) # TODO: validate this value against name.type
                break
        if not match_found:
            for regext, slug in url_map.items():
                doc_url.url = doc_url.url.strip()
                if re.search(regext, doc_url.url):
                    match_found = True
                    if slug:
                        stats['mapped'] +=1
                        name = ExtResourceName.objects.get(slug=slug)
                        # Munge the URL if it's the first github repo match
                        #  Remove "/tree/master" substring if it exists
                        #  Remove trailing "/issues" substring if it exists
                        #  Remove "/blob/master/.*" pattern if present
                        if regext == "https?://github\\.com":
                            doc_url.url = doc_url.url.replace("/tree/master","")
                            doc_url.url = re.sub('/issues$', '', doc_url.url)
                            doc_url.url = re.sub('/blob/master.*$', '', doc_url.url)
                        try:
                            validate_external_resource_value(name, doc_url.url)
                            DocExtResource.objects.create(doc=doc_url.doc, name=name, value=doc_url.url, display_name=doc_url.desc) # TODO: validate this value against name.type
                        except ValidationError as e: # pyflakes:ignore
                            debug.show('("Failed validation:", doc_url.url, e)')
                            stats['failed_validation'] +=1
                    else:
                        stats['ignored'] +=1
                    break
        if not match_found:
            debug.show('("Not Mapped:",doc_url.desc, doc_url.tag.slug, doc_url.doc.name, doc_url.url)')
            stats['not_mapped'] += 1
    print (stats)

def reverse(apps, schema_editor):
    DocExtResource = apps.get_model('doc', 'DocExtResource')
    DocExtResource.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0033_extres'),
        ('name', '0014_populate_extres'),
    ]

    operations = [
        migrations.RunPython(forward, reverse)
    ]
