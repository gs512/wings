# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields
import library.current_user
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library', '0002_auto_20140925_0257'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now_add=True)),
                ('uuid', django_extensions.db.fields.UUIDField(blank=True, editable=False, name='uuid')),
                ('is_locked', models.BooleanField(editable=False, default=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('created_by', models.ForeignKey(default=library.current_user.get_current_user, editable=False, to=settings.AUTH_USER_MODEL)),
                ('libraries', models.ManyToManyField(to='library.Library')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
