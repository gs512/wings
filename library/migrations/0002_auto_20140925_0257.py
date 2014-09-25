# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields
import library.current_user
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now_add=True)),
                ('uuid', django_extensions.db.fields.UUIDField(blank=True, editable=False, name='uuid')),
                ('is_locked', models.BooleanField(default=False, editable=False)),
                ('name', models.CharField(blank=True, null=True, max_length=255)),
                ('created_by', models.ForeignKey(default=library.current_user.get_current_user, editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TagValues',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now_add=True)),
                ('uuid', django_extensions.db.fields.UUIDField(blank=True, editable=False, name='uuid')),
                ('is_locked', models.BooleanField(default=False, editable=False)),
                ('name', models.CharField(blank=True, null=True, max_length=255)),
                ('tag_value', models.CharField(max_length=255)),
                ('tag_number', models.IntegerField()),
                ('created_by', models.ForeignKey(default=library.current_user.get_current_user, editable=False, to=settings.AUTH_USER_MODEL)),
                ('library', models.ForeignKey(to='library.Library')),
                ('tag', models.ForeignKey(to='library.Tag')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='tag',
            name='libraries_group',
            field=models.ManyToManyField(to='library.Library', through='library.TagValues'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='library',
            name='average_phred',
            field=models.CharField(blank=True, null=True, max_length=255, verbose_name='Average Phred'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='library',
            name='determined_reads',
            field=models.IntegerField(blank=True, null=True, verbose_name='Determined Reads #'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='library',
            name='ercc_dilution',
            field=models.FloatField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='library',
            name='ercc_mix',
            field=models.CharField(blank=True, null=True, max_length=10),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='library',
            name='ercc_r2',
            field=models.FloatField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='library',
            name='ercc_url',
            field=models.URLField(blank=True, null=True, verbose_name='ERCC URL'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='library',
            name='flowcell_id',
            field=models.CharField(blank=True, null=True, max_length=255, verbose_name='Flowcell Id'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='library',
            name='library_alias',
            field=models.TextField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='library',
            name='lld',
            field=models.IntegerField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='library',
            name='n',
            field=models.IntegerField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='library',
            name='name',
            field=models.CharField(blank=True, null=True, max_length=255),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='library',
            name='qc_report_url',
            field=models.URLField(blank=True, null=True, verbose_name='QC URL'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='library',
            name='reads_mapped_ercc',
            field=models.IntegerField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='library',
            name='reads_mapped_ercc_portion',
            field=models.FloatField(blank=True, null=True, verbose_name='Reads Mapped ERCC (%)'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='library',
            name='reads_mapped_refseq',
            field=models.IntegerField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='library',
            name='reads_type',
            field=models.CharField(null=True, max_length=255, verbose_name='Reads Type'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='library',
            name='replicate',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
