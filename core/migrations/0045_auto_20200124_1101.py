# Generated by Django 2.2.6 on 2020-01-24 11:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0044_merge_20200124_1041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurantcuisine',
            name='restaurant',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cuisines', to='core.Restaurant'),
        ),
    ]