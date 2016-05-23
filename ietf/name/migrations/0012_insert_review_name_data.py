# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def insert_initial_review_data(apps, schema_editor):
    ReviewRequestStateName = apps.get_model("name", "ReviewRequestStateName")
    ReviewRequestStateName.objects.get_or_create(slug="requested", name="Requested", order=1)
    ReviewRequestStateName.objects.get_or_create(slug="accepted", name="Accepted", order=2)
    ReviewRequestStateName.objects.get_or_create(slug="rejected", name="Rejected", order=3)
    ReviewRequestStateName.objects.get_or_create(slug="withdrawn", name="Withdrawn", order=4)
    ReviewRequestStateName.objects.get_or_create(slug="overtaken", name="Overtaken By Events", order=5)
    ReviewRequestStateName.objects.get_or_create(slug="noresponse", name="No Response", order=6)
    ReviewRequestStateName.objects.get_or_create(slug="part-completed", name="Partially Completed", order=6)
    ReviewRequestStateName.objects.get_or_create(slug="completed", name="Completed", order=8)


    ReviewTypeName = apps.get_model("name", "ReviewTypeName")
    ReviewTypeName.objects.get_or_create(slug="early", name="Early", order=1)
    ReviewTypeName.objects.get_or_create(slug="lc", name="Last Call", order=2)
    ReviewTypeName.objects.get_or_create(slug="telechat", name="Telechat", order=3)

    ReviewResultName = apps.get_model("name", "ReviewResultName")
    ReviewResultName.objects.get_or_create(slug="almost-ready", name="Almost Ready", order=1)
    ReviewResultName.objects.get_or_create(slug="issues", name="Has Issues", order=2)
    ReviewResultName.objects.get_or_create(slug="nits", name="Has Nits", order=3)
    ReviewResultName.objects.get_or_create(slug="not-ready", name="Not Ready", order=4)
    ReviewResultName.objects.get_or_create(slug="right-track", name="On the Right Track", order=5)
    ReviewResultName.objects.get_or_create(slug="ready", name="Ready", order=6)
    ReviewResultName.objects.get_or_create(slug="ready-issues", name="Ready with Issues", order=7)
    ReviewResultName.objects.get_or_create(slug="ready-nits", name="Ready with Nits", order=8)
    ReviewResultName.objects.get_or_create(slug="serious-issues", name="Serious Issues", order=9)

    RoleName = apps.get_model("name", "RoleName")
    RoleName.objects.get_or_create(slug="reviewer", name="Reviewer", order=max(r.order for r in RoleName.objects.all()) + 1)

def noop(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('name', '0011_reviewrequeststatename_reviewresultname_reviewtypename'),
        ('group', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(insert_initial_review_data, noop),
    ]
