# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-13 18:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip_generator', '0003_auto_20180513_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destination',
            name='trip_day_percentage',
            field=models.DecimalField(blank=True, decimal_places=6, default=None, max_digits=9, null=True),
        ),
    ]
