# Generated by Django 2.0 on 2018-03-21 17:23

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('virulence', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ariba',
            name='summary',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=[]),
        ),
    ]
