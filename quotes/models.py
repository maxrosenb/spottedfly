from django.db import models

class Playlist(models.Model):
	playlist_uri = models.CharField(max_length=100)

	def __str__(self):
		return self.playlist_uri
