# Generated by Django 2.0 on 2018-01-31 16:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('version', '0001_initial'),
        ('sample', '0003_auto_20171215_2005'),
        ('resistance', '0002_auto_20180131_1607'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='ariba',
            unique_together={('sample', 'version')},
        ),
        migrations.AlterUniqueTogether(
            name='aribasequence',
            unique_together={('sample', 'version')},
        ),
    ]
