# Generated by Django 2.2.7 on 2020-05-28 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0006_playlist_sus'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='quality',
            field=models.CharField(choices=[('TE', 'Terrible'), ('BA', 'Bad'), ('OK', 'Neutral'), ('GO', 'GOOD'), ('EX', 'EXCELLENT')], default='OK', max_length=2),
        ),
    ]
