from django.db import models
from django.core.validators import validate_comma_separated_integer_list

class Playlist(models.Model):
	playlist_uri = models.CharField(max_length=100)
	followers_list = models.CharField(validators=[validate_comma_separated_integer_list], max_length=50000)
	dates_list = models.CharField(validators=[validate_comma_separated_integer_list], max_length=50000)

	def __str__(self):
		return self.playlist_uri
