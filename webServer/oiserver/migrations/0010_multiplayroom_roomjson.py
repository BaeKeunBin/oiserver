# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-20 12:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oiserver', '0009_multiplayroom'),
    ]

    operations = [
        migrations.AddField(
            model_name='multiplayroom',
            name='roomJson',
            field=models.TextField(default='default'),
        ),
    ]
