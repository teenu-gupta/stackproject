# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20151113_1942'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='password',
        ),
    ]
