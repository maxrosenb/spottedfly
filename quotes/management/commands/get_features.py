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
    help = 'Set All Qualities'

    def handle(self, *args, **kwargs):

        queryset = Playlist.objects.all()
        for pl_result in queryset:
            print("URI: ", pl_result.playlist_uri)
            tracks = sp.playlist_tracks(pl_result.playlist_uri, fields=None, limit=10, offset=0, market=None, additional_types=('track', ))
            total_dance = 0
            total_energy = 0
            total_instrumentalness = 0
            total_valence = 0
            n = len(tracks["items"])
            for i in range(n):
                features = sp.audio_features(tracks["items"][i]['track']['external_urls']['spotify'])
                dance = features[0]['danceability']
                energy = features[0]['energy']
                instrumentalness = features[0]['instrumentalness']
                valence = features[0]['valence']
                total_dance += dance
                total_energy += energy
                total_instrumentalness += instrumentalness
                total_valence += valence
            avg_energy = round(total_energy / n, 2)
            avg_dance = round(total_dance / n, 2)
            avg_instrumentalness = round(total_instrumentalness / n, 2)
            avg_valence = round(total_valence / n, 2)
            pl_result.avg_dance = avg_dance
            pl_result.avg_energy = avg_energy
            pl_result.avg_instru = avg_instrumentalness
            pl_result.avg_valence = avg_valence
            pl_result.save()