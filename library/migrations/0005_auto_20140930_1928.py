# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_auto_20140925_1545'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='library',
            name='library_id',
        ),
        migrations.AlterField(
            model_name='library',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='tagvalues',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
