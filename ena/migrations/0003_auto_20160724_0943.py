# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-24 09:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ena', '0002_auto_20160724_0932'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='tosample',
            unique_together=set([('experiment_accession', 'server')]),
        ),
    ]
