# Generated by Django 2.2.6 on 2019-11-20 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20191114_0835'),
    ]

    operations = [
        migrations.RenameField(
            model_name='foodmenu',
            old_name='recipe',
            new_name='ingredients',
        ),
        migrations.AddField(
            model_name='foodcart',
            name='number_of_food',
            field=models.IntegerField(default=1),
        ),
    ]
