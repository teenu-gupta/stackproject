# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='is_email_verified',
            field=models.BooleanField(default=False, verbose_name='Email Verified'),
        ),
    ]
