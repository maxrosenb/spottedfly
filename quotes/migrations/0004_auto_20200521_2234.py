# Generated by Django 3.0.6 on 2020-05-22 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0003_playlist_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='dates_list',
            field=models.CharField(max_length=50000),
        ),
    ]
