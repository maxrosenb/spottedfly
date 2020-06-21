"""
Spottedfly views.py
"""

from datetime import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import validate_comma_separated_integer_list

class Playlist(models.Model):
    """Playlist Model for Database"""
    name = models.CharField(max_length=100)
    playlist_uri = models.CharField(max_length=100)
    followers_list = models.CharField(validators=[validate_comma_separated_integer_list], max_length=50000)
    dates_list = models.CharField(max_length=50000)
    qualities_list = models.CharField(max_length=50000, null=True)
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

    def __str__(self):
    	return self.playlist_uri

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
