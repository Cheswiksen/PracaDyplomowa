# Generated by Django 2.1.3 on 2018-12-04 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Site', '0006_auto_20181204_1035'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='services',
        ),
        migrations.AddField(
            model_name='car',
            name='services',
            field=models.ManyToManyField(to='Site.Service'),
        ),
    ]
