# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-11 20:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapper', '0005_remove_job_output_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='output_file',
            field=models.CharField(default='tmp.out', max_length=255),
        ),
    ]
