# Generated by Django 2.2.6 on 2020-01-28 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0046_order_paid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='location_text',
            new_name='address_line1',
        ),
        migrations.AddField(
            model_name='order',
            name='city',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='order',
            name='state',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='order',
            name='zip_code',
            field=models.CharField(default='', max_length=255),
        ),
    ]
