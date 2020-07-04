from __future__ import print_function
import binascii
import struct
from PIL import Image
import numpy as np
import scipy
import scipy.misc
import scipy.cluster
from django.core.management.base import BaseCommand
from quotes.models import Playlist
import colorthief

class Command(BaseCommand):
    help = 'Dominant color finder'

    def handle(self, *args, **kwargs):

        queryset = Playlist.objects.all()
        for pl in queryset:
            color_thief = colorthief.ColorThief(pl.photo)
            # get the dominant color
            dominant_color = color_thief.get_color(quality=1)
            print(pl.playlist_uri, pl.name, dominant_color,dominant_color[0], dominant_color[1],dominant_color[2])
            pl.photo_red = dominant_color[0]
            pl.photo_green = dominant_color[1]
            pl.photo_blue = dominant_color[2]
            pl.save()