# Generated by Django 2.0 on 2017-12-12 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlastQuery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('length', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('repo', models.TextField()),
                ('tag', models.TextField(unique=True)),
                ('sha256', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='version',
            unique_together={('repo', 'tag', 'sha256')},
        ),
        migrations.AlterUniqueTogether(
            name='blastquery',
            unique_together={('title', 'length')},
        ),
    ]
