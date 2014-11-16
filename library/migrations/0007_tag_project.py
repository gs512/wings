# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0006_attachment_flag_gene_exp_read_group_tracking'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='project',
            field=models.ForeignKey(to='library.Project', blank=True, null=True),
            preserve_default=True,
        ),
    ]
