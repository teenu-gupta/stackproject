# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_personimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='last_login',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login'),
        ),
    ]
