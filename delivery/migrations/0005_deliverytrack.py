# Generated by Django 2.2.6 on 2020-05-17 12:49

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0004_auto_20191226_0937'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryTrack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_location_point', django.contrib.gis.db.models.fields.PointField(blank=True, geography=True, null=True, srid=4326)),
                ('last_location_text', models.CharField(blank=True, max_length=255, null=True)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('delivery', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='track', to='delivery.Delivery')),
            ],
        ),
    ]
