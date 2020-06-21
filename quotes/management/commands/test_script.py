from django.core.management.base import BaseCommand, CommandError
from django.shortcuts import render
import requests
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import traceback
import logging
from datetime import datetime
from quotes.models import Playlist
from django_cron import CronJobBase, Schedule
from django.shortcuts import get_list_or_404, get_object_or_404
import io
from django.contrib.auth.decorators import login_required
import urllib, base64
max_client_id = '83403a77c90f4836b8287b70bac39a33'
max_client_secret = '48cd4347f180427fb116fd9376f10ca2'

client_credentials_manager = SpotifyClientCredentials(client_id=max_client_id,client_secret=max_client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):

        queryset = Playlist.objects.all()
        for playlist in queryset:
            if playlist.followers_list:
                playlist.followers_list += "," + str(sp.playlist(playlist.playlist_uri)['followers']['total'])
        	else:
        	    playlist.followers_list = str(sp.playlist(playlist.playlist_uri)['followers']['total'])
        	now = datetime.now()
        	if playlist.dates_list:
        	    playlist.dates_list += "," + now.strftime('%Y-%m-%d %H:%M:%S')
        	else:
        	    playlist.dates_list = now.strftime('%Y-%m-%d %H:%M:%S')
        	playlist.save()