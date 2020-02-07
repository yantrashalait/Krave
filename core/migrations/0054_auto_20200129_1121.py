# Generated by Django 2.2.6 on 2020-01-29 11:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0053_auto_20200129_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurantfoodcategory',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='food_category', to='core.Restaurant'),
        ),
    ]