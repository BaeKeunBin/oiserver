# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-01 15:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('oiserver', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roomJson', models.TextField()),
                ('isProfile', models.CharField(max_length=50)),
                ('userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oiserver.UserInfo')),
            ],
        ),
    ]
