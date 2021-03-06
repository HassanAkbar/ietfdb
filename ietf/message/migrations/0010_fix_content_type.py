# Copyright The IETF Trust 2020, All Rights Reserved
# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-21 14:27


from tqdm import tqdm

from django.db import migrations

import debug                            # pyflakes:ignore


def forward(apps, schema_editor):

    Message                     = apps.get_model('message', 'Message')

    for m in tqdm(Message.objects.filter(content_type='')):
        m.content_type = 'text/plain'
        m.save()

def reverse(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('message', '0009_fix_address_lists'),
    ]

    operations = [
        migrations.RunPython(forward, reverse),
    ]
