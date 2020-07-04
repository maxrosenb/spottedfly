# Generated by Django 3.0.6 on 2020-05-21 00:11

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='dates_list',
            field=models.CharField(default=2, max_length=50000, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='playlist',
            name='followers_list',
            field=models.CharField(default=2, max_length=50000, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')]),
            preserve_default=False,
        ),
    ]
