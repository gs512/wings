# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields
import library.current_user
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library', '0005_auto_20140930_1928'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('uuid', django_extensions.db.fields.UUIDField(name='uuid', editable=False, blank=True)),
                ('is_locked', models.BooleanField(default=False, editable=False)),
                ('last_modified', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('file', models.FileField(upload_to='files/%Y/%m/%d')),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, default=library.current_user.get_current_user, editable=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='flag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('uuid', django_extensions.db.fields.UUIDField(name='uuid', editable=False, blank=True)),
                ('is_locked', models.BooleanField(default=False, editable=False)),
                ('last_modified', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('flag', models.BooleanField(default=False, editable=False)),
                ('operation', models.CharField(max_length=100)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, default=library.current_user.get_current_user, editable=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='gene_exp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('uuid', django_extensions.db.fields.UUIDField(name='uuid', editable=False, blank=True)),
                ('is_locked', models.BooleanField(default=False, editable=False)),
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
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, default=library.current_user.get_current_user, editable=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='read_group_tracking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('uuid', django_extensions.db.fields.UUIDField(name='uuid', editable=False, blank=True)),
                ('is_locked', models.BooleanField(default=False, editable=False)),
                ('last_modified', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('tracking_id', models.CharField(max_length=100)),
                ('condition', models.CharField(max_length=100)),
                ('replicate', models.IntegerField(default=0)),
                ('FPKM', models.FloatField(default=0)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, default=library.current_user.get_current_user, editable=False)),
                ('project', models.ForeignKey(to='library.Project')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
