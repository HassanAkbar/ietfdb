# Copyright The IETF Trust 2018-2020, All Rights Reserved
# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-20 10:52


import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import ietf.utils.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('name', '0001_initial'),
        ('person', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BallotType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField()),
                ('name', models.CharField(max_length=255)),
                ('question', models.TextField(blank=True)),
                ('used', models.BooleanField(default=True)),
                ('order', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='DeletedEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('json', models.TextField(help_text='Deleted object in JSON format, with attribute names chosen to be suitable for passing into the relevant create method.')),
                ('time', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='DocAlias',
            fields=[
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'document alias',
                'verbose_name_plural': 'document aliases',
            },
        ),
        migrations.CreateModel(
            name='DocEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(db_index=True, default=datetime.datetime.now, help_text='When the event happened')),
                ('type', models.CharField(choices=[(b'new_revision', b'Added new revision'), (b'new_submission', b'Uploaded new revision'), (b'changed_document', b'Changed document metadata'), (b'added_comment', b'Added comment'), (b'added_message', b'Added message'), (b'edited_authors', b'Edited the documents author list'), (b'deleted', b'Deleted document'), (b'changed_state', b'Changed state'), (b'changed_stream', b'Changed document stream'), (b'expired_document', b'Expired document'), (b'extended_expiry', b'Extended expiry of document'), (b'requested_resurrect', b'Requested resurrect'), (b'completed_resurrect', b'Completed resurrect'), (b'changed_consensus', b'Changed consensus'), (b'published_rfc', b'Published RFC'), (b'added_suggested_replaces', b'Added suggested replacement relationships'), (b'reviewed_suggested_replaces', b'Reviewed suggested replacement relationships'), (b'changed_group', b'Changed group'), (b'changed_protocol_writeup', b'Changed protocol writeup'), (b'changed_charter_milestone', b'Changed charter milestone'), (b'initial_review', b'Set initial review time'), (b'changed_review_announcement', b'Changed WG Review text'), (b'changed_action_announcement', b'Changed WG Action text'), (b'started_iesg_process', b'Started IESG process on document'), (b'created_ballot', b'Created ballot'), (b'closed_ballot', b'Closed ballot'), (b'sent_ballot_announcement', b'Sent ballot announcement'), (b'changed_ballot_position', b'Changed ballot position'), (b'changed_ballot_approval_text', b'Changed ballot approval text'), (b'changed_ballot_writeup_text', b'Changed ballot writeup text'), (b'changed_rfc_editor_note_text', b'Changed RFC Editor Note text'), (b'changed_last_call_text', b'Changed last call text'), (b'requested_last_call', b'Requested last call'), (b'sent_last_call', b'Sent last call'), (b'scheduled_for_telechat', b'Scheduled for telechat'), (b'iesg_approved', b'IESG approved document (no problem)'), (b'iesg_disapproved', b'IESG disapproved document (do not publish)'), (b'approved_in_minute', b'Approved in minute'), (b'iana_review', b'IANA review comment'), (b'rfc_in_iana_registry', b'RFC is in IANA registry'), (b'rfc_editor_received_announcement', b'Announcement was received by RFC Editor'), (b'requested_publication', b'Publication at RFC Editor requested'), (b'sync_from_rfc_editor', b'Received updated information from RFC Editor'), (b'requested_review', b'Requested review'), (b'assigned_review_request', b'Assigned review request'), (b'closed_review_request', b'Closed review request'), (b'downref_approved', b'Downref approved')], max_length=50)),
                ('rev', models.CharField(blank=True, max_length=16, null=True, verbose_name='revision')),
                ('desc', models.TextField()),
            ],
            options={
                'ordering': ['-time', '-id'],
            },
        ),
        migrations.CreateModel(
            name='DocHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=datetime.datetime.now)),
                ('title', models.CharField(max_length=255, validators=[django.core.validators.RegexValidator(message='Please enter a string without control characters.', regex='^[^\x00-\x1f]*$')])),
                ('abstract', models.TextField(blank=True)),
                ('rev', models.CharField(blank=True, max_length=16, verbose_name='revision')),
                ('pages', models.IntegerField(blank=True, null=True)),
                ('words', models.IntegerField(blank=True, null=True)),
                ('order', models.IntegerField(blank=True, default=1)),
                ('expires', models.DateTimeField(blank=True, null=True)),
                ('notify', models.CharField(blank=True, max_length=255)),
                ('external_url', models.URLField(blank=True)),
                ('note', models.TextField(blank=True)),
                ('internal_comments', models.TextField(blank=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'document history',
                'verbose_name_plural': 'document histories',
            },
        ),
        migrations.CreateModel(
            name='DocHistoryAuthor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('affiliation', models.CharField(blank=True, help_text='Organization/company used by author for submission', max_length=100)),
                ('country', models.CharField(blank=True, help_text='Country used by author for submission', max_length=255)),
                ('order', models.IntegerField(default=1)),
            ],
            options={
                'ordering': ['document', 'order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DocReminder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('due', models.DateTimeField()),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('time', models.DateTimeField(default=datetime.datetime.now)),
                ('title', models.CharField(max_length=255, validators=[django.core.validators.RegexValidator(message='Please enter a string without control characters.', regex='^[^\x00-\x1f]*$')])),
                ('abstract', models.TextField(blank=True)),
                ('rev', models.CharField(blank=True, max_length=16, verbose_name='revision')),
                ('pages', models.IntegerField(blank=True, null=True)),
                ('words', models.IntegerField(blank=True, null=True)),
                ('order', models.IntegerField(blank=True, default=1)),
                ('expires', models.DateTimeField(blank=True, null=True)),
                ('notify', models.CharField(blank=True, max_length=255)),
                ('external_url', models.URLField(blank=True)),
                ('note', models.TextField(blank=True)),
                ('internal_comments', models.TextField(blank=True)),
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator(b'^[-a-z0-9]+$', b'Provide a valid document name consisting of lowercase letters, numbers and hyphens.', b'invalid')])),
                ('ad', ietf.utils.models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ad_document_set', to='person.Person', verbose_name='area director')),
                ('formal_languages', models.ManyToManyField(blank=True, help_text='Formal languages used in document', to='name.FormalLanguageName')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DocumentAuthor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('affiliation', models.CharField(blank=True, help_text='Organization/company used by author for submission', max_length=100)),
                ('country', models.CharField(blank=True, help_text='Country used by author for submission', max_length=255)),
                ('order', models.IntegerField(default=1)),
                ('document', ietf.utils.models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doc.Document')),
                ('email', ietf.utils.models.ForeignKey(blank=True, help_text='Email address used by author for submission', null=True, on_delete=django.db.models.deletion.CASCADE, to='person.Email')),
                ('person', ietf.utils.models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='person.Person')),
            ],
            options={
                'ordering': ['document', 'order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DocumentURL',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(blank=True, default='', max_length=255)),
                ('url', models.URLField(max_length=512)),
                ('doc', ietf.utils.models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doc.Document')),
                ('tag', ietf.utils.models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='name.DocUrlTagName')),
            ],
        ),
        migrations.CreateModel(
            name='RelatedDocHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relationship', ietf.utils.models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='name.DocRelationshipName')),
                ('source', ietf.utils.models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doc.DocHistory')),
                ('target', ietf.utils.models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reversely_related_document_history_set', to='doc.DocAlias')),
            ],
        ),
        migrations.CreateModel(
            name='RelatedDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relationship', ietf.utils.models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='name.DocRelationshipName')),
                ('source', ietf.utils.models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doc.Document')),
                ('target', ietf.utils.models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doc.DocAlias')),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField()),
                ('name', models.CharField(max_length=255)),
                ('used', models.BooleanField(default=True)),
                ('desc', models.TextField(blank=True)),
                ('order', models.IntegerField(default=0)),
                ('next_states', models.ManyToManyField(blank=True, related_name='previous_states', to='doc.State')),
            ],
            options={
                'ordering': ['type', 'order'],
            },
        ),
        migrations.CreateModel(
            name='StateType',
            fields=[
                ('slug', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('label', models.CharField(help_text='Label that should be used (e.g. in admin) for state drop-down for this type of state', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='AddedMessageEvent',
            fields=[
                ('docevent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='doc.DocEvent')),
                ('msgtype', models.CharField(max_length=25)),
            ],
            bases=('doc.docevent',),
        ),
        migrations.CreateModel(
            name='BallotDocEvent',
            fields=[
                ('docevent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='doc.DocEvent')),
            ],
            bases=('doc.docevent',),
        ),
        migrations.CreateModel(
            name='BallotPositionDocEvent',
            fields=[
                ('docevent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='doc.DocEvent')),
                ('discuss', models.TextField(blank=True, help_text='Discuss text if position is discuss')),
                ('discuss_time', models.DateTimeField(blank=True, help_text='Time discuss text was written', null=True)),
                ('comment', models.TextField(blank=True, help_text='Optional comment')),
                ('comment_time', models.DateTimeField(blank=True, help_text='Time optional comment was written', null=True)),
            ],
            bases=('doc.docevent',),
        ),
        migrations.CreateModel(
            name='ConsensusDocEvent',
            fields=[
                ('docevent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='doc.DocEvent')),
                ('consensus', models.NullBooleanField(default=None)),
            ],
            bases=('doc.docevent',),
        ),
        migrations.CreateModel(
            name='EditedAuthorsDocEvent',
            fields=[
                ('docevent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='doc.DocEvent')),
                ('basis', models.CharField(help_text='What is the source or reasoning for the changes to the author list', max_length=255)),
            ],
            bases=('doc.docevent',),
        ),
        migrations.CreateModel(
            name='InitialReviewDocEvent',
            fields=[
                ('docevent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='doc.DocEvent')),
                ('expires', models.DateTimeField(blank=True, null=True)),
            ],
            bases=('doc.docevent',),
        ),
        migrations.CreateModel(
            name='LastCallDocEvent',
            fields=[
                ('docevent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='doc.DocEvent')),
                ('expires', models.DateTimeField(blank=True, null=True)),
            ],
            bases=('doc.docevent',),
        ),
        migrations.CreateModel(
            name='NewRevisionDocEvent',
            fields=[
                ('docevent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='doc.DocEvent')),
            ],
            bases=('doc.docevent',),
        ),
        migrations.CreateModel(
            name='ReviewRequestDocEvent',
            fields=[
                ('docevent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='doc.DocEvent')),
            ],
            bases=('doc.docevent',),
        ),
        migrations.CreateModel(
            name='StateDocEvent',
            fields=[
                ('docevent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='doc.DocEvent')),
            ],
            bases=('doc.docevent',),
        ),
        migrations.CreateModel(
            name='SubmissionDocEvent',
            fields=[
                ('docevent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='doc.DocEvent')),
            ],
            bases=('doc.docevent',),
        ),
        migrations.CreateModel(
            name='TelechatDocEvent',
            fields=[
                ('docevent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='doc.DocEvent')),
                ('telechat_date', models.DateField(blank=True, null=True)),
                ('returning_item', models.BooleanField(default=False)),
            ],
            bases=('doc.docevent',),
        ),
        migrations.CreateModel(
            name='WriteupDocEvent',
            fields=[
                ('docevent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='doc.DocEvent')),
                ('text', models.TextField(blank=True)),
            ],
            bases=('doc.docevent',),
        ),
        migrations.AddField(
            model_name='state',
            name='type',
            field=ietf.utils.models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doc.StateType'),
        ),
    ]
