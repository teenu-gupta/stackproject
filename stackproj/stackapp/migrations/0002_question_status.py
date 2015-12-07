# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stackapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='status',
            field=models.CharField(default=b'raised', max_length=200, null=True, blank=True, choices=[(b'raised', 'Raised'), (b'posted', 'Posted'), (b'answered', 'Answered'), (b'irrelevant', 'Irrelevant')]),
        ),
    ]
