# Generated by Django 4.1 on 2022-10-10 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='end_time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='start_time',
            field=models.TimeField(null=True),
        ),
    ]
