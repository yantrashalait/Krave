# Generated by Django 2.2.6 on 2020-05-17 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0069_auto_20200403_0625'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='delivery_person',
        ),
    ]
