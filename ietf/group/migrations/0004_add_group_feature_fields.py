# Copyright The IETF Trust 2019, All Rights Reserved
# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-01-10 07:51
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0003_groupfeatures_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupfeatures',
            name='acts_like_wg',
            field=models.BooleanField(default=False, verbose_name=b'WG-Like'),
        ),
        migrations.AddField(
            model_name='groupfeatures',
            name='create_wiki',
            field=models.BooleanField(default=False, verbose_name=b'Wiki'),
        ),
        migrations.AddField(
            model_name='groupfeatures',
            name='custom_group_roles',
            field=models.BooleanField(default=False, verbose_name=b'Group Roles'),
        ),
        migrations.AddField(
            model_name='groupfeatures',
            name='has_session_materials',
            field=models.BooleanField(default=False, verbose_name=b'Materials'),
        ),
        migrations.AddField(
            model_name='groupfeatures',
            name='is_schedulable',
            field=models.BooleanField(default=False, verbose_name=b'Schedulable'),
        ),
        migrations.AddField(
            model_name='groupfeatures',
            name='role_order',
            field=models.CharField(default=b'chair,secr,member', help_text=b'The order in which roles are shown, for instance on photo pages', max_length=128, validators=[django.core.validators.RegexValidator(code=b'invalid', message=b'Enter a comma-separated list of role slugs', regex=b'[a-z0-9_-]+(,[a-z0-9_-]+)*')]),
        ),
        migrations.AddField(
            model_name='groupfeatures',
            name='show_on_agenda',
            field=models.BooleanField(default=False, verbose_name=b'On Agenda'),
        ),
        migrations.AddField(
            model_name='groupfeatures',
            name='req_subm_approval',
            field=models.BooleanField(default=False, verbose_name=b'Subm. Approval'),
        ),
        migrations.AddField(
            model_name='groupfeatures',
            name='matman_roles',
            field=models.CharField(default=b'ad,chair,delegate,secr', max_length=64, validators=[django.core.validators.RegexValidator(code=b'invalid', message=b'Enter a comma-separated list of role slugs', regex=b'[a-z0-9_-]+(,[a-z0-9_-]+)*')]),
        ),
        migrations.AddField(
            model_name='historicalgroupfeatures',
            name='acts_like_wg',
            field=models.BooleanField(default=False, verbose_name=b'WG-Like'),
        ),
        migrations.AddField(
            model_name='historicalgroupfeatures',
            name='create_wiki',
            field=models.BooleanField(default=False, verbose_name=b'Wiki'),
        ),
        migrations.AddField(
            model_name='historicalgroupfeatures',
            name='custom_group_roles',
            field=models.BooleanField(default=False, verbose_name=b'Group Roles'),
        ),
        migrations.AddField(
            model_name='historicalgroupfeatures',
            name='has_session_materials',
            field=models.BooleanField(default=False, verbose_name=b'Materials'),
        ),
        migrations.AddField(
            model_name='historicalgroupfeatures',
            name='is_schedulable',
            field=models.BooleanField(default=False, verbose_name=b'Schedulable'),
        ),
        migrations.AddField(
            model_name='historicalgroupfeatures',
            name='role_order',
            field=models.CharField(default=b'chair,secr,member', help_text=b'The order in which roles are shown, for instance on photo pages', max_length=128, validators=[django.core.validators.RegexValidator(code=b'invalid', message=b'Enter a comma-separated list of role slugs', regex=b'[a-z0-9_-]+(,[a-z0-9_-]+)*')]),
        ),
        migrations.AddField(
            model_name='historicalgroupfeatures',
            name='show_on_agenda',
            field=models.BooleanField(default=False, verbose_name=b'On Agenda'),
        ),
        migrations.AddField(
            model_name='historicalgroupfeatures',
            name='req_subm_approval',
            field=models.BooleanField(default=False, verbose_name=b'Subm. Approval'),
        ),
        migrations.AddField(
            model_name='historicalgroupfeatures',
            name='matman_roles',
            field=models.CharField(default=b'ad,chair,delegate,secr', max_length=64, validators=[django.core.validators.RegexValidator(code=b'invalid', message=b'Enter a comma-separated list of role slugs', regex=b'[a-z0-9_-]+(,[a-z0-9_-]+)*')]),
        ),
    ]
