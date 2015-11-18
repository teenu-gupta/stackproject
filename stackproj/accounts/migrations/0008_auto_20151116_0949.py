# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import accounts.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_remove_person_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personimage',
            name='image',
            field=models.FileField(null=True, upload_to=accounts.models.profile_image_path, blank=True),
        ),
    ]
