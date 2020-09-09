# Generated by Django 2.2.6 on 2020-09-09 06:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0078_auto_20200909_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodmenu',
            name='main_category',
            field=models.ForeignKey(blank=True, help_text='If no suitable category is found, create a restaurant category.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='food', to='core.Category'),
        ),
        migrations.AlterField(
            model_name='foodmenu',
            name='rest_category',
            field=models.ForeignKey(blank=True, help_text='Will be seen inside restaurant detail page.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='food', to='core.RestaurantFoodCategory'),
        ),
    ]
