# Generated by Django 2.2.6 on 2020-09-07 16:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0076_foodmenu_chef_special'),
    ]

    operations = [
        migrations.RenameField(
            model_name='foodmenu',
            old_name='category',
            new_name='main_category',
        ),
    ]