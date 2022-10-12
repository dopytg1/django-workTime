# Generated by Django 4.1 on 2022-10-11 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_worktime_flag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worktime',
            name='created_at',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='worktime',
            name='end_time',
            field=models.TimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='worktime',
            name='start_time',
            field=models.TimeField(auto_now=True),
        ),
    ]