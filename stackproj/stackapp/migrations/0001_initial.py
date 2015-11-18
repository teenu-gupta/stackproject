# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('created_date', models.DateField(auto_now=True)),
                ('answered_by', models.ForeignKey(related_name='answered_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Hashtags',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('created_date', models.DateField(auto_now=True)),
                ('asked_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('hashtag', models.ManyToManyField(to='stackapp.Hashtags', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vote_type', models.SmallIntegerField(default=True, blank=True, choices=[(0, b'Downvote'), (1, b'Upvote')])),
                ('answer', models.ForeignKey(to='stackapp.Answer', null=True)),
                ('question', models.ForeignKey(to='stackapp.Question', null=True)),
                ('voted_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(related_name='answer_of', to='stackapp.Question'),
        ),
    ]
