# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-12-15 08:19
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
import ietf.person.models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0020_auto_20170701_0325'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalApiKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('endpoint', models.CharField(choices=[(b'/api/iesg/position', b'/api/iesg/position')], max_length=128)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('valid', models.BooleanField(default=True)),
                ('salt', models.BinaryField(default=ietf.person.models.salt, max_length=12)),
                ('count', models.IntegerField(default=0)),
                ('latest', models.DateTimeField(blank=True, null=True)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apikeys', to='person.Person')),
            ],
        ),
        migrations.CreateModel(
            name='PersonEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=datetime.datetime.now, help_text=b'When the event happened')),
                ('type', models.CharField(choices=[(b'apikey_login', b'API key login')], max_length=50)),
                ('desc', models.TextField()),
            ],
            options={
                'ordering': ['-time', '-id'],
            },
        ),
        migrations.CreateModel(
            name='PersonApiKeyEvent',
            fields=[
                ('personevent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='person.PersonEvent')),
                ('key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='person.PersonalApiKey')),
            ],
            bases=('person.personevent',),
        ),
        migrations.AddField(
            model_name='personevent',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='person.Person'),
        ),
    ]
