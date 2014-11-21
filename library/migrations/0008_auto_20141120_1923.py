# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0007_tag_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='gene_exp',
            name='fpkm_1',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gene_exp',
            name='fpkm_2',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gene_exp',
            name='inf',
            field=models.BooleanField(default=False, editable=False),
            preserve_default=True,
        ),
    ]
