# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-07 21:35
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coment',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 7, 21, 35, 36, 691588, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 7, 21, 35, 36, 690171, tzinfo=utc)),
        ),
    ]