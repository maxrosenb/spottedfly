# Generated by Django 2.2.7 on 2020-06-21 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0014_auto_20200621_1018'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='avg_valence',
            field=models.FloatField(default=0),
        ),
    ]
