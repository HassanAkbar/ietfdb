# Copyright The IETF Trust 2018-2020, All Rights Reserved
# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-20 10:52


from typing import List, Tuple      # pyflakes:ignore

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]                                   # type: List[Tuple[str]]

    operations = [
        migrations.CreateModel(
            name='DumpInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('host', models.CharField(max_length=128)),
                ('tz', models.CharField(default='UTC', max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='VersionInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now=True)),
                ('command', models.CharField(max_length=32)),
                ('switch', models.CharField(max_length=16)),
                ('version', models.CharField(max_length=64)),
                ('used', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'VersionInfo',
            },
        ),
    ]
