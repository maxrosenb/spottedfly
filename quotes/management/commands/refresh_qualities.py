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
import os

MAX_CLIENT_ID = os.getenv("MAX_CLIENT_ID")
MAX_CLIENT_SECRET = os.getenv("MAX_CLIENT_SECRET")

class Command(BaseCommand):
    help = 'Set All Qualities'

    def handle(self, *args, **kwargs):

        queryset = Playlist.objects.all()
        for playlist in queryset:
            differences = []
            followers_unstrung = [int(x) for x in playlist.followers_list.split(',')]
            if len(followers_unstrung) > 24:
                followers_unstrung = followers_unstrung[-24:]
                for i in range(1,len(followers_unstrung)):
         	        differences.append(followers_unstrung[i] - followers_unstrung[i - 1])
                total = sum(differences)
                if total > 200:
                    playlist.quality = Playlist.EXCELLENT
                elif total > 50:
                    playlist.quality = Playlist.GOOD
                elif total > 25:
                    playlist.quality = Playlist.OK
                elif total > 10:
                    playlist.quality = Playlist.BAD
                else:
                    playlist.quality = Playlist.TERRIBLE
            else:
                playlist.quality = Playlist.TBA
            playlist.save()