# Copyright The IETF Trust 2021 All Rights Reserved

# Generated by Django 2.2.23 on 2021-05-21 13:29

from django.db import migrations

def forward(apps, schema_editor):
    StateType = apps.get_model('doc', 'StateType')
    State = apps.get_model('doc', 'State')

    StateType.objects.create(slug='bofreq', label='BOF Request State')
    proposed = State.objects.create(type_id='bofreq', slug='proposed', name='Proposed', used=True, desc='The BOF request is proposed', order=0)
    approved = State.objects.create(type_id='bofreq', slug='approved', name='Approved', used=True, desc='The BOF request is approved', order=1)
    declined = State.objects.create(type_id='bofreq', slug='declined', name='Declined', used=True, desc='The BOF request is declined', order=2)
    replaced = State.objects.create(type_id='bofreq', slug='replaced', name='Replaced', used=True, desc='The BOF request is proposed', order=3)
    abandoned = State.objects.create(type_id='bofreq', slug='abandoned', name='Abandoned', used=True, desc='The BOF request is abandoned', order=4)

    proposed.next_states.set([approved,declined,replaced,abandoned])

def reverse(apps, schema_editor):
    StateType = apps.get_model('doc', 'StateType')
    State = apps.get_model('doc', 'State')
    State.objects.filter(type_id='bofreq').delete()
    StateType.objects.filter(slug='bofreq').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0041_add_documentactionholder'),
        ('name', '0027_add_bofrequest'),
    ]

    operations = [
        migrations.RunPython(forward, reverse)
    ]
