# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-04 13:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sccmec', '0002_coverage_per_base_coverage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perbasecoverage',
            name='cassette',
        ),
        migrations.RemoveField(
            model_name='perbasecoverage',
            name='sample',
        ),
        migrations.DeleteModel(
            name='PerBaseCoverage',
        ),
    ]
