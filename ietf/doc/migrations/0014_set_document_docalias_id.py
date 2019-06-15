# Copyright The IETF Trust 2019, All Rights Reserved
# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-08 08:42
from __future__ import unicode_literals

import sys

from tqdm import tqdm

from django.db import migrations


def forward(apps, schema_editor):
    Document = apps.get_model('doc','Document')
    sys.stderr.write('\n')
    for i, d in enumerate(tqdm(Document.objects.all()), start=1):
        d.id = i
        d.save()

    DocAlias = apps.get_model('doc','DocAlias')
    for i, d in enumerate(tqdm(DocAlias.objects.all()), start=1):
        d.id = i
        d.save()

def reverse(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0013_add_document_docalias_id'),
    ]

    operations = [
        migrations.RunPython(forward, reverse),
    ]
