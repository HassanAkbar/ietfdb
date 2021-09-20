# Generated by Django 2.2.24 on 2021-09-20 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0019_auto_20210604_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalapikey',
            name='endpoint',
            field=models.CharField(choices=[('/api/appauth/authortools', '/api/appauth/authortools'), ('/api/iesg/position', '/api/iesg/position'), ('/api/meeting/session/video/url', '/api/meeting/session/video/url'), ('/api/notify/meeting/bluesheet', '/api/notify/meeting/bluesheet'), ('/api/notify/meeting/registration', '/api/notify/meeting/registration'), ('/api/v2/person/person', '/api/v2/person/person')], max_length=128),
        ),
    ]
