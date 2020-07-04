from django.core.files import File
from django.core.management.base import BaseCommand
import urllib.request
import os
from quotes.models import Playlist

class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):

        queryset = Playlist.objects.all()
        for playlist in queryset:
                result = urllib.request.urlretrieve(playlist.picture_url)
                playlist.photo.save(
                    os.path.basename(playlist.picture_url),
                    File(open(result[0], 'rb'))
                    )
                playlist.photo.save(os.path.basename(playlist.playlist_uri),File(open(result[0], 'rb')))
                playlist.save()
