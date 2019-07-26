# -*- coding: utf-8 -*-
#Copyright The IETF Trust 2019, All Rights Reserved
# Generated by Django 1.11.22 on 2019-07-22 11:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0018_document_primary_key_cleanup'),
    ]

    operations = [
        migrations.AddField(
            model_name='slidesubmission',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]