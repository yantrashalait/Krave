# Generated by Django 2.2.6 on 2020-01-08 05:36

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_order_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='location_point',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, geography=True, null=True, srid=4326),
        ),
        migrations.AddField(
            model_name='order',
            name='location_text',
            field=models.CharField(default='', max_length=255),
        ),
    ]
