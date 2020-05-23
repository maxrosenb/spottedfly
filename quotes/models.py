"""
Spottedfly views.py
"""

from django.db import models
from django.core.validators import validate_comma_separated_integer_list
from datetime import datetime
class Playlist(models.Model):
	"""Playlist Model for Database"""
	name = models.CharField(max_length=100)
	playlist_uri = models.CharField(max_length=100)
	followers_list = models.CharField(validators=[validate_comma_separated_integer_list], max_length=50000)
	dates_list = models.CharField(max_length=50000)

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
		self.approved_comment = True
		self.save()

	def __str__(self):
		return self.text