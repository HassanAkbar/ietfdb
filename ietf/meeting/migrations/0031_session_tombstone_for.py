# Copyright The IETF Trust 2020, All Rights Reserved

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0030_allow_empty_joint_with_sessions'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='tombstone_for',
            field=models.ForeignKey(blank=True, help_text='This session is the tombstone for a session that was rescheduled', null=True, on_delete=django.db.models.deletion.CASCADE, to='meeting.Session'),
        ),
    ]
