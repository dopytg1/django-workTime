# Generated by Django 4.1 on 2022-10-12 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_worktime_late_alter_worktime_on_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='worktime',
            name='late',
        ),
        migrations.RemoveField(
            model_name='worktime',
            name='on_time',
        ),
        migrations.AddField(
            model_name='member',
            name='late',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='on_time',
            field=models.IntegerField(null=True),
        ),
    ]
