# Generated by Django 2.2.7 on 2019-12-02 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Registration', '0010_auto_20191202_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeslot',
            name='date_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='end_time',
            field=models.TimeField(),
        ),
    ]
