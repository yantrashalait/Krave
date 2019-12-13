# Generated by Django 2.2.6 on 2019-12-13 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20191213_0749'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodmenu',
            name='calories',
            field=models.FloatField(blank=True, help_text='calories contained in this food', null=True),
        ),
        migrations.CreateModel(
            name='FoodCustomize',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_of_ingredient', models.CharField(help_text='Name of ingredient that can be added', max_length=500)),
                ('cost_of_addition', models.FloatField(help_text='Cost of additional ingredient per unit(in dollars)')),
                ('type', models.IntegerField(choices=[(1, 'optional'), (2, 'required')])),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customizes', to='core.FoodMenu')),
            ],
        ),
    ]
