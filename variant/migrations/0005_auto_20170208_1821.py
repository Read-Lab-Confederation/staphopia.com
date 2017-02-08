# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-02-08 18:21
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0007_remove_sample_db_tag'),
        ('variant', '0004_auto_20170207_2225'),
    ]

    operations = [
        migrations.CreateModel(
            name='ToIndelJSON',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('indels', django.contrib.postgres.fields.jsonb.JSONField(default=b'{}')),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sample.Sample')),
            ],
        ),
        migrations.AddField(
            model_name='indel',
            name='members',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=b'[]'),
        ),
    ]
