# Copyright The IETF Trust 2019, All Rights Reserved
# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-22 08:01


from __future__ import absolute_import, print_function, unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0004_1_del_docs_m2m_table'),
    ]

    # The implementation of AlterField in Django 1.11 applies
    #   'ALTER TABLE <table> MODIFY <field> ...;' in order to fix foregn keys
    #   to the altered field, but as it seems does _not_ fix up m2m
    #   intermediary tables in an equivalent manner, so here we remove and
    #   then recreate the m2m tables so they will have the appropriate field
    #   types.

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='related_docs',
        ),
        migrations.AddField(
            model_name='message',
            name='related_docs',
            field=models.ManyToManyField(blank=True, to='doc.Document'),
        ),
    ]
