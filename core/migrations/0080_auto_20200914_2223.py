# Generated by Django 2.2.6 on 2020-09-14 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0079_auto_20200909_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(blank=True, choices=[(0, 'Pending'), (1, 'Checked Out'), (2, 'Approved'), (3, 'Rejected'), (4, 'Prepared'), (5, 'Picked'), (6, 'Delivered')], null=True),
        ),
    ]
