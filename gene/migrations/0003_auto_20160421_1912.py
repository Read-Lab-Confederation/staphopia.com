# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-21 19:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gene', '0002_auto_20160420_1225'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inference', models.TextField(db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.TextField(db_index=True)),
            ],
        ),
        migrations.AddField(
            model_name='features',
            name='is_rRNA',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='features',
            name='inference',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='gene.Inference'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='features',
            name='note',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='gene.Note'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='features',
            name='product',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='gene.Product'),
            preserve_default=False,
        ),
    ]
