# Generated by Django 2.2.6 on 2019-12-14 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20191214_0719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodmenu',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='food', to='core.RestaurantFoodCategory'),
        ),
        migrations.AlterField(
            model_name='restaurantfoodcategory',
            name='category',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.DeleteModel(
            name='FoodCategory',
        ),
    ]
