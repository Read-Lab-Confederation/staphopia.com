# Generated by Django 2.0 on 2017-12-15 20:05

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sample', '0002_md5'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='sample',
            unique_together={('user', 'name')},
        ),
    ]
