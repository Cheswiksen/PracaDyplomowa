# Generated by Django 2.1.3 on 2018-12-04 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Site', '0005_auto_20181125_1127'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='buy_date',
        ),
        migrations.RemoveField(
            model_name='car',
            name='engine_float',
        ),
        migrations.RemoveField(
            model_name='car',
            name='mileage_number',
        ),
        migrations.RemoveField(
            model_name='car',
            name='production_date',
        ),
        migrations.RemoveField(
            model_name='car',
            name='registration_text',
        ),
        migrations.RemoveField(
            model_name='car',
            name='vin_text',
        ),
        migrations.RemoveField(
            model_name='car',
            name='services',
        ),
        migrations.AddField(
            model_name='car',
            name='services',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Site.Service'),
        ),
    ]