# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2018-02-22 05:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Benefit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False)),
                ('text', models.CharField(help_text='Display table etc.', max_length=255)),
                ('price', models.FloatField()),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BenefitLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False)),
                ('text', models.CharField(help_text='EG Gold, Silver, etc', max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Benefit Levels',
                'ordering': ('order',),
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='benefit',
            name='benefit_level',
            field=models.ManyToManyField(blank=True, related_name='levels', to='sponsorbenefits.BenefitLevel'),
        ),
    ]
