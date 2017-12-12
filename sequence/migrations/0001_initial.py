# Generated by Django 2.0 on 2017-12-12 22:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sample', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Summary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_paired', models.BooleanField(db_index=True, default=False)),
                ('rank', models.PositiveSmallIntegerField(db_index=True)),
                ('total_bp', models.BigIntegerField()),
                ('coverage', models.DecimalField(decimal_places=2, max_digits=7)),
                ('read_total', models.BigIntegerField(default=0)),
                ('read_min', models.PositiveIntegerField(default=0)),
                ('read_mean', models.DecimalField(decimal_places=4, default=0.0, max_digits=11)),
                ('read_std', models.DecimalField(decimal_places=4, default=0.0, max_digits=11)),
                ('read_median', models.PositiveIntegerField(default=0)),
                ('read_max', models.PositiveIntegerField(default=0)),
                ('read_25th', models.PositiveIntegerField(default=0)),
                ('read_75th', models.PositiveIntegerField(default=0)),
                ('read_lengths', models.TextField()),
                ('qual_mean', models.DecimalField(decimal_places=4, max_digits=7)),
                ('qual_std', models.DecimalField(decimal_places=4, max_digits=7)),
                ('qual_median', models.PositiveIntegerField()),
                ('qual_25th', models.PositiveIntegerField()),
                ('qual_75th', models.PositiveIntegerField()),
                ('qual_per_base', models.TextField()),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sequence_summary_sample', to='sample.Sample')),
                ('stage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sequence.Stage')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='summary',
            unique_together={('sample', 'stage')},
        ),
    ]
