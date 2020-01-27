# Generated by Django 2.2.6 on 2020-01-24 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0042_auto_20200116_1111'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cuisine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='restaurantcuisine',
            name='name',
        ),
        migrations.AddField(
            model_name='restaurantcuisine',
            name='cuisine',
            field=models.ManyToManyField(to='core.Cuisine'),
        ),
    ]
