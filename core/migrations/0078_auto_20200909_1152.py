# Generated by Django 2.2.6 on 2020-09-09 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0077_auto_20200907_2241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(blank=True, choices=[(0, 'Pending'), (1, 'Checked Out'), (2, 'Approved'), (3, 'Rejected'), (4, 'Prepared')], null=True),
        ),
    ]
