# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-21 21:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0003_program'),
        ('gene', '0003_auto_20160421_1912'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlastResults',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bitscore', models.PositiveSmallIntegerField()),
                ('evalue', models.DecimalField(decimal_places=2, max_digits=7)),
                ('identity', models.PositiveSmallIntegerField()),
                ('mismatch', models.PositiveSmallIntegerField()),
                ('gaps', models.PositiveSmallIntegerField()),
                ('hamming_distance', models.PositiveSmallIntegerField()),
                ('query_from', models.PositiveSmallIntegerField()),
                ('query_to', models.PositiveSmallIntegerField()),
                ('hit_from', models.PositiveIntegerField()),
                ('hit_to', models.PositiveIntegerField()),
                ('align_len', models.PositiveSmallIntegerField()),
                ('qseq', models.TextField()),
                ('hseq', models.TextField()),
                ('midline', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='features',
            name='prokka_id',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='blastresults',
            name='feature',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gene.Features'),
        ),
        migrations.AddField(
            model_name='blastresults',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sample.Program'),
        ),
        migrations.AddField(
            model_name='blastresults',
            name='sample',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sample.MetaData'),
        ),
        migrations.AlterUniqueTogether(
            name='blastresults',
            unique_together=set([('sample', 'feature')]),
        ),
    ]
