# Generated by Django 2.2.6 on 2019-12-26 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_auto_20191226_0937'),
    ]

    operations = [
        migrations.RenameField(
            model_name='restaurantrequest',
            old_name='location',
            new_name='location_point',
        ),
        migrations.AddField(
            model_name='restaurantrequest',
            name='location_text',
            field=models.CharField(default='', max_length=500),
        ),
    ]
