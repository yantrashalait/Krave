# Generated by Django 2.2.6 on 2020-04-02 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0066_auto_20200325_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment',
            field=models.IntegerField(blank=True, choices=[(1, 'On Delivery'), (2, 'Card')], null=True),
        ),
    ]
