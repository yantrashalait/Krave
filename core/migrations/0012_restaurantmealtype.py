# Generated by Django 2.2.6 on 2019-11-13 06:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_foodmenu_meal_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='RestaurantMealType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meal_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='restaurant', to='core.MealType')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meal', to='core.Restaurant')),
            ],
        ),
    ]