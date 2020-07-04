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
MAX_CLIENT_ID = os.getenv("MAX_CLIENT_ID")
MAX_CLIENT_SECRET = os.getenv("MAX_CLIENT_SECRET")

client_credentials_manager = SpotifyClientCredentials(client_id=max_client_id,client_secret=max_client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):

        queryset = Playlist.objects.all()
        for playlist in queryset:
        	if playlist.quality == Playlist.TBA:
        	    continue
        	elif playlist.quality == Playlist.TERRIBLE:
        	    if playlist.qualities_list:
        	        playlist.qualities_list += "1,"
        	    else:
        	        playlist.qualities_list = "1,"
        	elif playlist.quality == Playlist.BAD:
        	    if playlist.qualities_list:
        	        playlist.qualities_list += "2,"
        	    else:
        	        playlist.qualities_list = "2,"
        	elif playlist.quality == Playlist.OK:
        	    if playlist.qualities_list:
        	        playlist.qualities_list += "3,"
        	    else:
        	        playlist.qualities_list = "3,"
        	elif playlist.quality == Playlist.GOOD:
        	    if playlist.qualities_list:
        	        playlist.qualities_list += "4,"
        	    else:
        	        playlist.qualities_list = "4,"
        	elif playlist.quality == Playlist.EXCELLENT:
        	    if playlist.qualities_list:
        	        playlist.qualities_list += "5,"
        	    else:
        	        playlist.qualities_list = "5,"
        	playlist.save()