# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-05-25 21:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('variant', '0009_reference_sequence'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotation',
            name='phase',
            field=models.SmallIntegerField(default=0),
        ),
    ]
