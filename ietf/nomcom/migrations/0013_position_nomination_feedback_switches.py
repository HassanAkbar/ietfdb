# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-19 07:58
from __future__ import unicode_literals

from django.db import migrations, models
from django.db.models import F

def forward(apps, schema_editor):
    Position = apps.get_model('nomcom','Position')
    Position.objects.update(accepting_nominations=F('is_open'))
    Position.objects.update(accepting_feedback=F('is_open'))

def reverse(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('nomcom', '0012_auto_20170210_0205'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='accepting_feedback',
            field=models.BooleanField(default=False, verbose_name=b'Is accepting feedback'),
        ),
        migrations.AddField(
            model_name='position',
            name='accepting_nominations',
            field=models.BooleanField(default=False, verbose_name=b'Is accepting nominations'),
        ),
        migrations.RunPython(forward,reverse)
    ]
