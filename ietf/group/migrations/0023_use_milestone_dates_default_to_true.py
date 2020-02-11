# -*- coding: utf-8 -*-
# Copyright The IETF Trust 2020, All Rights Reserved
# Generated by Django 1.11.28 on 2020-02-11 07:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0022_populate_uses_milestone_dates'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='uses_milestone_dates',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='grouphistory',
            name='uses_milestone_dates',
            field=models.BooleanField(default=True),
        ),
    ]
