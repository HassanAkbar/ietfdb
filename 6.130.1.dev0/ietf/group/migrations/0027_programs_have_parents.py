# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-05-08 09:02
from __future__ import unicode_literals

from django.db import migrations

def forward(apps, schema_editor):
    Group = apps.get_model('group','Group')
    iab = Group.objects.get(acronym='iab')
    Group.objects.filter(type_id='program').update(parent=iab)

def reverse(apps, schema_editor):
    pass # No point in removing the parents

class Migration(migrations.Migration):

    dependencies = [
        ('group', '0026_programs_meet'),
    ]

    operations = [
        migrations.RunPython(forward, reverse),
    ]
