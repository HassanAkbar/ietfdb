# Copyright The IETF Trust 2019-2020, All Rights Reserved
# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-08 11:58


from django.db import migrations
import django.db.models.deletion
import ietf.utils.models


class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0015_1_add_fk_to_document_id'),
        ('liaisons', '0002_auto_20180225_1207'),
    ]

    operations = [
        migrations.AddField(
            model_name='liaisonstatementattachment',
            name='document2',
            field=ietf.utils.models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='doc.Document', to_field=b'id'),
        ),
        migrations.AlterField(
            model_name='liaisonstatementattachment',
            name='document',
            field=ietf.utils.models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='old_liaison', to='doc.Document', to_field=b'name'),
        ),
    ]
