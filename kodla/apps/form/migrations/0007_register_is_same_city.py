# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2018-03-30 11:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0006_auto_20180330_1425'),
    ]

    operations = [
        migrations.AddField(
            model_name='register',
            name='is_same_city',
            field=models.BooleanField(default=False, verbose_name='Same City'),
        ),
    ]