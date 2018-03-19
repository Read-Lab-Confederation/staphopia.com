# Generated by Django 2.0 on 2018-03-19 20:24

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mlst', '0003_auto_20171215_0654'),
    ]

    operations = [
        migrations.CreateModel(
            name='Support',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ariba', models.PositiveIntegerField(default=0)),
                ('mentalist', models.PositiveIntegerField(default=0)),
                ('blast', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='mlst',
            name='is_novel',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name='report',
            name='ariba',
            field=django.contrib.postgres.fields.jsonb.JSONField(),
        ),
        migrations.AlterField(
            model_name='report',
            name='blast',
            field=django.contrib.postgres.fields.jsonb.JSONField(),
        ),
        migrations.AlterField(
            model_name='report',
            name='mentalist',
            field=django.contrib.postgres.fields.jsonb.JSONField(),
        ),
        migrations.AlterUniqueTogether(
            name='support',
            unique_together={('ariba', 'mentalist', 'blast')},
        ),
    ]
