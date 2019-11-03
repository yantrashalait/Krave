# Generated by Django 2.2.6 on 2019-11-01 07:27

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_restaurantrequest_rejected'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, geography=True, null=True, srid=4326),
        ),
    ]