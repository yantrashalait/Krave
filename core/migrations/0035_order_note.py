# Generated by Django 2.2.6 on 2020-01-07 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_remove_restaurant_delivery_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='note',
            field=models.TextField(default=''),
        ),
    ]