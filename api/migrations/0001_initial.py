# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-04 23:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Jaunt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('live', models.BooleanField()),
                ('owner', models.IntegerField()),
                ('title', models.CharField(max_length=256)),
                ('shortcode', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('jaunt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Jaunt')),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('owner', models.IntegerField()),
                ('original_url', models.CharField(max_length=512)),
                ('thumbnail_url', models.CharField(max_length=512)),
                ('taken_at', models.DateTimeField()),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('deleted', models.BooleanField()),
                ('jaunt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Jaunt')),
            ],
        ),
    ]
