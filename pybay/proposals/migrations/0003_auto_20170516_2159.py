# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-05-17 01:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0002_auto_20170419_0634'),
    ]

    operations = [
        migrations.AddField(
            model_name='talkproposal',
            name='meetup_talk',
            field=models.CharField(choices=[(1, 'Yes'), (2, 'Maybe'), (3, 'No')], default='No', max_length=100),
        ),
        migrations.AddField(
            model_name='tutorialproposal',
            name='meetup_talk',
            field=models.CharField(choices=[(1, 'Yes'), (2, 'Maybe'), (3, 'No')], default='No', max_length=100),
        ),
        migrations.AlterField(
            model_name='talkproposal',
            name='category',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='talkproposal',
            name='talk_links',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='tutorialproposal',
            name='category',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='tutorialproposal',
            name='talk_links',
            field=models.CharField(max_length=200),
        ),
    ]
