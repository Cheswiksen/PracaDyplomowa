# Generated by Django 2.1.3 on 2018-11-21 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Site', '0003_auto_20181120_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='mark_text',
            field=models.CharField(default='mark', max_length=32),
        ),
        migrations.AddField(
            model_name='car',
            name='model_text',
            field=models.CharField(default='model', max_length=32),
        ),
    ]
