# Copyright The IETF Trust 2018-2020, All Rights Reserved
# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-03 06:39


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0005_fix_replaced_iab_irtf_stream_docs'),
    ]

    operations = [
        migrations.AddField(
            model_name='ballotpositiondocevent',
            name='send_email',
            field=models.NullBooleanField(default=None),
        ),
    ]
