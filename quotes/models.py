"""
Spottedfly views.py
"""

import os
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.files import File
from django.core.validators import validate_comma_separated_integer_list
from taggit.managers import TaggableManager
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import urllib
import colorthief

MAX_CLIENT_ID='83403a77c90f4836b8287b70bac39a33'
MAX_CLIENT_SECRET='48cd4347f180427fb116fd9376f10ca2'

client_credentials_manager = SpotifyClientCredentials(client_id=MAX_CLIENT_ID,client_secret=MAX_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

class Playlist(models.Model):
    """Playlist Model for Database"""
    name = models.CharField(max_length=100)
    playlist_uri = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='images/', blank=True)
    tags = TaggableManager()
    followers_list = models.CharField(validators=[validate_comma_separated_integer_list], max_length=50000)
    dates_list = models.CharField(max_length=50000)
    sus = models.BooleanField()
    avg_dance = models.FloatField(default=0)
    avg_energy = models.FloatField(default=0)
    avg_instru = models.FloatField(default = 0)
    avg_valence = models.FloatField(default = 0)
    TERRIBLE = 'TE'
    BAD = 'BA'
    OK = 'OK'
    GOOD = 'GO'
    EXCELLENT = 'EX'
    TBA = 'TB'
    QUALITY_CHOICES = (
	    (TERRIBLE, 'Terrible'),
	    (BAD, 'Bad'),
	    (OK, 'Neutral'),
	    (GOOD, 'Good'),
	    (EXCELLENT, 'Excellent'),
	    (TBA, 'Tba'),
    )
    quality = models.CharField(max_length=2, choices=QUALITY_CHOICES, default = TBA)
    seven_day_quality = models.CharField(max_length=2, choices=QUALITY_CHOICES, default = TBA)
    picture_url = models.CharField(max_length=10000, blank=True)
    photo_red = models.FloatField(default=125)
    photo_green = models.FloatField(default=255)
    photo_blue = models.FloatField(default=78)

    def __str__(self):
    	return self.playlist_uri

    def save(self, *args, **kwargs):
        print("SAVING!!!!")
        if not self.pk:
            super().save(*args, **kwargs)
            picture_url = sp.playlist(self.playlist_uri)['images'][0]['url']
            tracks = sp.playlist_tracks(self.playlist_uri, fields=None, limit=10, offset=0, market=None, additional_types=('track', ))
            total_dance = 0
            total_energy = 0
            total_instrumentalness = 0
            total_valence = 0
            n = len(tracks["items"])

            for i in range(n):
                features = sp.audio_features(tracks["items"][i]['track']['external_urls']['spotify'])

                if features[0] is not None:
                    dance = features[0]['danceability']
                    energy = features[0]['energy']
                    instrumentalness = features[0]['instrumentalness']
                    valence = features[0]['valence']

                else:
                    dance = 0
                    energy = 0
                    instrumentalness = 0
                    valence = 0

                total_dance += dance
                total_energy += energy
                total_instrumentalness += instrumentalness
                total_valence += valence

                avg_energy = round(total_energy / n, 2)
                avg_dance = round(total_dance / n, 2)
                avg_instrumentalness = round(total_instrumentalness / n, 2)
                avg_valence = round(total_valence / n, 2)

                self.avg_dance = avg_dance
                self.avg_energy = avg_energy
                self.avg_instru = avg_instrumentalness
                self.avg_valence = avg_valence

            print(picture_url)
            result = urllib.request.urlretrieve(picture_url)
            self.photo.save(os.path.basename(self.playlist_uri),File(open(result[0], 'rb')))
            color_thief = colorthief.ColorThief(self.photo)
            dominant_color = color_thief.get_color(quality=1)
            self.photo_red = dominant_color[0]
            self.photo_green = dominant_color[1]
            self.photo_blue = dominant_color[2]
        return super(Playlist, self).save(*args, **kwargs)




class Comment(models.Model):
    """Comments for the Playlist Page"""
    post = models.ForeignKey('quotes.Playlist', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=datetime.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
    	"""Approve Comment"""
    	self.approved_comment = True
    	self.save()

    def __str__(self):
    	""" str rep """
    	return self.text

class Profile(models.Model):
    """Profile class to extend User Model"""
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    library = models.ManyToManyField(Playlist)
