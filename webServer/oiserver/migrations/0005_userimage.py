# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-09 08:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oiserver', '0004_userroom_roomname'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userID', models.CharField(max_length=200)),
                ('imageData', models.ImageField(upload_to='image/')),
            ],
        ),
    ]