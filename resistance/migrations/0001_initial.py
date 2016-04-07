# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-07 16:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gene', '0001_initial'),
        ('variant', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gene',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('product', models.TextField()),
                ('dna', models.TextField()),
                ('aa', models.TextField()),
                ('cluster', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='gene.Clusters')),
            ],
        ),
        migrations.CreateModel(
            name='Genotype',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Name',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Phenotype',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('predicted_mic', models.TextField()),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resistance.Name')),
            ],
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pmid', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ToSNP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('snp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resistance_snp', to='variant.SNP')),
            ],
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField()),
                ('substitution', models.TextField()),
                ('gene', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resistance.Gene')),
            ],
        ),
        migrations.AddField(
            model_name='tosnp',
            name='variant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resistance.Variant'),
        ),
        migrations.AddField(
            model_name='phenotype',
            name='publication',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resistance.Publication'),
        ),
        migrations.AddField(
            model_name='genotype',
            name='phenotype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resistance.Phenotype'),
        ),
        migrations.AddField(
            model_name='genotype',
            name='variant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resistance.Variant'),
        ),
    ]
