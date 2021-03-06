# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-13 18:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip_generator', '0002_auto_20180513_1723'),
    ]

    operations = [
        migrations.RenameField(
            model_name='destination',
            old_name='trip_day_ratio',
            new_name='trip_day_percentage',
        ),
        migrations.AddField(
            model_name='trip',
            name='number_of_days',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
