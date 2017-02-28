# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-28 10:46
from __future__ import unicode_literals

from django.db import migrations
from collections import Counter

import debug    # pyflakes:ignore

def repair_primary(apps, schema_editor):
    Person = apps.get_model('person','Person')
    Email = apps.get_model('person','Email')
    for p in Person.objects.all():
        primary = p.email_set.filter(primary=True).first()
        if primary and not primary.active:
            #debug.show("['removing primary',primary.address,p.name]")
            primary.primary = False
            primary.save()
            new_primary = p.email_set.filter(active=True).order_by("-time").first()
            if new_primary:
                #debug.show("['adding primary',new_primary.address,p.name]")
                new_primary.primary = True
                new_primary.save()
    for p_id in [x for x in Counter(Email.objects.filter(primary=True).values_list('person',flat=True)).items() if x[1]>1]:
        for e in Email.objects.filter(person_id=p_id,primary=True)[1:]:
            #debug.show("['removing extra primary', e.address, e.person.name]")
            e.primary = False
            e.save()

def do_nothing(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('person', '0014_auto_20160613_0751'),
    ]

    operations = [
        migrations.RunPython(repair_primary,do_nothing)
    ]
