# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-14 00:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trip_generator', '0004_auto_20180513_1858'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TripDay',
            new_name='ItineraryDay',
        ),
    ]
