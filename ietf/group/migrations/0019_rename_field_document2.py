# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-25 06:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0019_rename_field_document2'),
        ('group', '0018_remove_old_document_field'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='charter2',
            new_name='charter',
        ),
    ]
