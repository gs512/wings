# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='library',
            name='reads_mapped_refseq_portion',
            field=models.FloatField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='library',
            name='name',
            field=models.CharField(blank=True, editable=False, null=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(blank=True, editable=False, null=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(blank=True, editable=False, null=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='tagvalues',
            name='name',
            field=models.CharField(blank=True, editable=False, null=True, max_length=255),
        ),
    ]
