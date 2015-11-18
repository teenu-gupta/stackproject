# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import accounts.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_person_is_email_verified'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(null=True, upload_to=accounts.models.profile_image_path, blank=True)),
                ('owner', models.OneToOneField(related_name='profile_image', to='accounts.Person')),
            ],
        ),
    ]
