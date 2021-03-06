# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-13 02:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Accommodation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=128)),
                ('price', models.DecimalField(decimal_places=2, max_digits=50)),
                ('check_in_datetime', models.DateTimeField()),
                ('check_out_datetime', models.DateTimeField()),
                ('city', models.CharField(max_length=128)),
                ('country', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=128)),
                ('country', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_time', models.DateTimeField()),
                ('return_time', models.DateTimeField()),
                ('origin', models.CharField(max_length=128)),
                ('destination', models.CharField(max_length=128)),
                ('price', models.DecimalField(decimal_places=2, max_digits=50)),
            ],
        ),
        migrations.CreateModel(
            name='Itinerary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_date', models.DateField()),
                ('return_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='TripDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('accommodations', models.ManyToManyField(to='trip_generator.Accommodation')),
                ('destinations', models.ManyToManyField(to='trip_generator.Destination')),
                ('flight', models.ManyToManyField(to='trip_generator.Flight')),
                ('itinerary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trip_generator.Itinerary')),
            ],
        ),
        migrations.AddField(
            model_name='itinerary',
            name='trip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trip_generator.Trip'),
        ),
        migrations.AddField(
            model_name='destination',
            name='trip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trip_generator.Trip'),
        ),
    ]
