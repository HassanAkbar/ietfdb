# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-21 05:31
from __future__ import unicode_literals

import sys, time

from django.db import migrations

def timestamp(apps, schema_editor):
    sys.stderr.write('\n %s' % time.strftime('%Y-%m-%d %H:%M:%S'))

class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0019_rename_field_document2'),
    ]

    operations = [
        # Copy the doc IDs from the explicit m2m table to the implicit table
        migrations.RunPython(timestamp, timestamp),
        migrations.RunSQL(
            "INSERT INTO doc_document_formal_languages SELECT id,document_id,formallanguagename_id FROM doc_documentlanguages;",
            ""),
        migrations.RunPython(timestamp, timestamp),
        migrations.RunSQL(
            "INSERT INTO doc_document_states SELECT id,document_id,state_id FROM doc_documentstates;",
            ""),
        migrations.RunPython(timestamp, timestamp),
        migrations.RunSQL(
            "INSERT INTO doc_document_tags SELECT id,document_id,doctagname_id FROM doc_documenttags;",
            ""),
        migrations.RunPython(timestamp, timestamp),
    ]
