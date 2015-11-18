# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_person_last_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='password',
            field=models.CharField(default=datetime.datetime(2015, 11, 12, 15, 58, 14, 567961, tzinfo=utc), max_length=128, verbose_name='Password'),
            preserve_default=False,
        ),
    ]
