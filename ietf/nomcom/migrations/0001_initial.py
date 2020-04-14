# Copyright The IETF Trust 2018-2020, All Rights Reserved
# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-20 10:52


from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import ietf.nomcom.fields
import ietf.nomcom.models
import ietf.utils.models
import ietf.utils.storage


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('group', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dbtemplate', '0001_initial'),
        ('name', '0001_initial'),
        ('person', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.EmailField(blank=True, max_length=254, verbose_name='Author')),
                ('subject', models.TextField(blank=True, verbose_name='Subject')),
                ('comments', ietf.nomcom.fields.EncryptedTextField(verbose_name='Comments')),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['time'],
            },
        ),
        migrations.CreateModel(
            name='FeedbackLastSeen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='NomCom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_key', models.FileField(blank=True, null=True, storage=ietf.utils.storage.NoLocationMigrationFileSystemStorage(location=None), upload_to=ietf.nomcom.models.upload_path_handler)),
                ('send_questionnaire', models.BooleanField(default=False, help_text='If you check this box, questionnaires are sent automatically after nominations.', verbose_name='Send questionnaires automatically')),
                ('reminder_interval', models.PositiveIntegerField(blank=True, help_text='If the nomcom user sets the interval field then a cron command will send reminders to the nominees who have not responded using the following formula: (today - nomination_date) % interval == 0.', null=True)),
                ('initial_text', models.TextField(blank=True, verbose_name='Help text for nomination form')),
                ('show_nominee_pictures', models.BooleanField(default=True, help_text='Display pictures of each nominee (if available) on the feedback pages', verbose_name='Show nominee pictures')),
                ('group', ietf.utils.models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='group.Group')),
            ],
            options={
                'verbose_name': 'NomCom',
                'verbose_name_plural': 'NomComs',
            },
        ),
        migrations.CreateModel(
            name='Nomination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('candidate_name', models.CharField(max_length=255, verbose_name='Candidate name')),
                ('candidate_email', models.EmailField(max_length=255, verbose_name='Candidate email')),
                ('candidate_phone', models.CharField(blank=True, max_length=255, verbose_name='Candidate phone')),
                ('nominator_email', models.EmailField(blank=True, max_length=254, verbose_name='Nominator Email')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('share_nominator', models.BooleanField(default=False, help_text='Check this box to allow the NomCom to let the person you are nominating know that you were one of the people who nominated them. If you do not check this box, your name will be confidential and known only within NomCom.', verbose_name='Share nominator name with candidate')),
                ('comments', ietf.utils.models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nomcom.Feedback')),
            ],
            options={
                'verbose_name_plural': 'Nominations',
            },
        ),
        migrations.CreateModel(
            name='Nominee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duplicated', ietf.utils.models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='nomcom.Nominee')),
                ('email', ietf.utils.models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='person.Email')),
                ('nomcom', ietf.utils.models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nomcom.NomCom')),
            ],
            options={
                'ordering': ['-nomcom__group__acronym', 'email__address'],
                'verbose_name_plural': 'Nominees',
            },
        ),
        migrations.CreateModel(
            name='NomineePosition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('nominee', ietf.utils.models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nomcom.Nominee')),
            ],
            options={
                'ordering': ['nominee'],
                'verbose_name': 'Nominee position',
                'verbose_name_plural': 'Nominee positions',
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='This short description will appear on the Nomination and Feedback pages. Be as descriptive as necessary. Past examples: "Transport AD", "IAB Member"', max_length=255, verbose_name='Name')),
                ('is_open', models.BooleanField(default=False, help_text='Set is_open when the nomcom is working on a position. Clear it when an appointment is confirmed.', verbose_name='Is open')),
                ('accepting_nominations', models.BooleanField(default=False, verbose_name='Is accepting nominations')),
                ('accepting_feedback', models.BooleanField(default=False, verbose_name='Is accepting feedback')),
                ('nomcom', ietf.utils.models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nomcom.NomCom')),
                ('questionnaire', ietf.utils.models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questionnaire', to='dbtemplate.DBTemplate')),
                ('requirement', ietf.utils.models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='requirement', to='dbtemplate.DBTemplate')),
            ],
            options={
                'verbose_name_plural': 'Positions',
            },
        ),
        migrations.CreateModel(
            name='ReminderDates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('nomcom', ietf.utils.models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nomcom.NomCom')),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(help_text='This short description will appear on the Feedback pages.', max_length=255, verbose_name='Name')),
                ('accepting_feedback', models.BooleanField(default=False, verbose_name='Is accepting feedback')),
                ('audience', ietf.utils.models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='name.TopicAudienceName')),
                ('description', ietf.utils.models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='description', to='dbtemplate.DBTemplate')),
                ('nomcom', ietf.utils.models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nomcom.NomCom')),
            ],
            options={
                'verbose_name_plural': 'Topics',
            },
        ),
        migrations.CreateModel(
            name='TopicFeedbackLastSeen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now=True)),
                ('reviewer', ietf.utils.models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='person.Person')),
                ('topic', ietf.utils.models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nomcom.Topic')),
            ],
        ),
        migrations.AddField(
            model_name='nomineeposition',
            name='position',
            field=ietf.utils.models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nomcom.Position'),
        ),
        migrations.AddField(
            model_name='nomineeposition',
            name='state',
            field=ietf.utils.models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='name.NomineePositionStateName'),
        ),
        migrations.AddField(
            model_name='nominee',
            name='nominee_position',
            field=models.ManyToManyField(through='nomcom.NomineePosition', to='nomcom.Position'),
        ),
        migrations.AddField(
            model_name='nominee',
            name='person',
            field=ietf.utils.models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='person.Person'),
        ),
        migrations.AddField(
            model_name='nomination',
            name='nominee',
            field=ietf.utils.models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nomcom.Nominee'),
        ),
        migrations.AddField(
            model_name='nomination',
            name='position',
            field=ietf.utils.models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nomcom.Position'),
        ),
        migrations.AddField(
            model_name='nomination',
            name='user',
            field=ietf.utils.models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='feedbacklastseen',
            name='nominee',
            field=ietf.utils.models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nomcom.Nominee'),
        ),
        migrations.AddField(
            model_name='feedbacklastseen',
            name='reviewer',
            field=ietf.utils.models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='person.Person'),
        ),
        migrations.AddField(
            model_name='feedback',
            name='nomcom',
            field=ietf.utils.models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nomcom.NomCom'),
        ),
        migrations.AddField(
            model_name='feedback',
            name='nominees',
            field=models.ManyToManyField(blank=True, to='nomcom.Nominee'),
        ),
        migrations.AddField(
            model_name='feedback',
            name='positions',
            field=models.ManyToManyField(blank=True, to='nomcom.Position'),
        ),
        migrations.AddField(
            model_name='feedback',
            name='topics',
            field=models.ManyToManyField(blank=True, to='nomcom.Topic'),
        ),
        migrations.AddField(
            model_name='feedback',
            name='type',
            field=ietf.utils.models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='name.FeedbackTypeName'),
        ),
        migrations.AddField(
            model_name='feedback',
            name='user',
            field=ietf.utils.models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='nomineeposition',
            unique_together=set([('position', 'nominee')]),
        ),
        migrations.AlterUniqueTogether(
            name='nominee',
            unique_together=set([('email', 'nomcom')]),
        ),
    ]
