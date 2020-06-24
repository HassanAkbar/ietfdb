# Copyright The IETF Trust 2019-2020, All Rights Reserved
# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2018-12-28 13:11


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0007_idexists'),
    ]

    operations = [
        migrations.AddField(
            model_name='dochistory',
            name='uploaded_filename',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='document',
            name='uploaded_filename',
            field=models.TextField(blank=True),
        ),
    ]
