# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import library.current_user
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Library',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now_add=True)),
                ('uuid', django_extensions.db.fields.UUIDField(blank=True, name='uuid', editable=False)),
                ('is_locked', models.BooleanField(default=False, editable=False)),
                ('library_id', models.CharField(verbose_name='Library ID', max_length=255)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, default=library.current_user.get_current_user, editable=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
