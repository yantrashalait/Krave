# Generated by Django 2.2.6 on 2020-06-06 05:38

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_auto_20200606_0519'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='userlocationtrack',
            managers=[
                ('location_manager', django.db.models.manager.Manager()),
            ],
        ),
    ]
