# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_person_password'),
    ]

    operations = [
        migrations.RenameField(
            model_name='person',
            old_name='username',
            new_name='owner',
        ),
    ]
