# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import library.current_user
from django.conf import settings
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('uuid', django_extensions.db.fields.UUIDField(editable=False, name='uuid', blank=True)),
                ('is_locked', models.BooleanField(editable=False, default=False)),
                ('last_modified', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('file', models.FileField(upload_to='files/%Y/%m/%d')),
                ('created_by', models.ForeignKey(default=library.current_user.get_current_user, editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='flag',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('uuid', django_extensions.db.fields.UUIDField(editable=False, name='uuid', blank=True)),
                ('is_locked', models.BooleanField(editable=False, default=False)),
                ('last_modified', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('flag', models.BooleanField(editable=False, default=False)),
                ('operation', models.CharField(max_length=100)),
                ('created_by', models.ForeignKey(default=library.current_user.get_current_user, editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='gene_exp',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('uuid', django_extensions.db.fields.UUIDField(editable=False, name='uuid', blank=True)),
                ('is_locked', models.BooleanField(editable=False, default=False)),
                ('last_modified', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('test_id', models.CharField(max_length=100)),
                ('sample_1', models.CharField(max_length=100)),
                ('sample_2', models.CharField(max_length=100)),
                ('p_value', models.FloatField(default=0)),
                ('q_value', models.FloatField(default=0)),
                ('FC', models.FloatField(default=0)),
                ('SEM_1', models.FloatField(default=0)),
                ('SEM_2', models.FloatField(default=0)),
                ('fpkm_1', models.FloatField(default=0)),
                ('fpkm_2', models.FloatField(default=0)),
                ('inf', models.BooleanField(editable=False, default=False)),
                ('created_by', models.ForeignKey(default=library.current_user.get_current_user, editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Library',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('uuid', django_extensions.db.fields.UUIDField(editable=False, name='uuid', blank=True)),
                ('is_locked', models.BooleanField(editable=False, default=False)),
                ('last_modified', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('reads_type', models.CharField(max_length=255, null=True, verbose_name='Reads Type')),
                ('flowcell_id', models.CharField(max_length=255, null=True, verbose_name='Flowcell Id', blank=True)),
                ('determined_reads', models.IntegerField(null=True, verbose_name='Determined Reads #', blank=True)),
                ('average_phred', models.CharField(max_length=255, null=True, verbose_name='Average Phred', blank=True)),
                ('qc_report_url', models.URLField(null=True, verbose_name='QC URL', blank=True)),
                ('ercc_r2', models.FloatField(null=True, blank=True)),
                ('ercc_mix', models.CharField(max_length=10, null=True, blank=True)),
                ('ercc_dilution', models.FloatField(null=True, blank=True)),
                ('reads_mapped_refseq_portion', models.FloatField(null=True, blank=True)),
                ('reads_mapped_ercc', models.IntegerField(null=True, blank=True)),
                ('reads_mapped_ercc_portion', models.FloatField(null=True, verbose_name='Reads Mapped ERCC (%)', blank=True)),
                ('n', models.IntegerField(null=True, blank=True)),
                ('ercc_url', models.URLField(null=True, verbose_name='ERCC URL', blank=True)),
                ('library_alias', models.TextField(null=True, blank=True)),
                ('reads_mapped_refseq', models.IntegerField(null=True, blank=True)),
                ('lld', models.IntegerField(null=True, blank=True)),
                ('replicate', models.IntegerField(default=1)),
                ('created_by', models.ForeignKey(default=library.current_user.get_current_user, editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('uuid', django_extensions.db.fields.UUIDField(editable=False, name='uuid', blank=True)),
                ('is_locked', models.BooleanField(editable=False, default=False)),
                ('last_modified', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('created_by', models.ForeignKey(default=library.current_user.get_current_user, editable=False, to=settings.AUTH_USER_MODEL)),
                ('libraries', models.ManyToManyField(to='library.Library')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='read_group_tracking',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('uuid', django_extensions.db.fields.UUIDField(editable=False, name='uuid', blank=True)),
                ('is_locked', models.BooleanField(editable=False, default=False)),
                ('last_modified', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('tracking_id', models.CharField(max_length=100)),
                ('condition', models.CharField(max_length=100)),
                ('replicate', models.IntegerField(default=0)),
                ('FPKM', models.FloatField(default=0)),
                ('created_by', models.ForeignKey(default=library.current_user.get_current_user, editable=False, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(to='library.Project')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('uuid', django_extensions.db.fields.UUIDField(editable=False, name='uuid', blank=True)),
                ('is_locked', models.BooleanField(editable=False, default=False)),
                ('last_modified', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('uuid', django_extensions.db.fields.UUIDField(editable=False, name='uuid', blank=True)),
                ('is_locked', models.BooleanField(editable=False, default=False)),
                ('last_modified', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
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
            model_name='tag',
            name='project',
            field=models.ForeignKey(blank=True, to='library.Project', null=True),
            preserve_default=True,
        ),
    ]
