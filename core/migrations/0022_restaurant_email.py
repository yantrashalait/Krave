# Generated by Django 2.2.6 on 2019-12-14 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_restaurantimage_main_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='email',
            field=models.CharField(default='', max_length=500),
        ),
    ]
