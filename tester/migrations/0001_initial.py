# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-09-18 20:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('access_token', models.CharField(max_length=2048)),
                ('refresh_token', models.CharField(max_length=2048)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
    ]
