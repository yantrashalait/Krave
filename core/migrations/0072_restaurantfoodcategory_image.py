# Generated by Django 2.2.6 on 2020-06-26 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0071_restaurantpayment'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurantfoodcategory',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='restaurant/category/'),
        ),
    ]
