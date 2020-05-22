from django.shortcuts import render
import requests
import json
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import traceback
import logging
from datetime import datetime
from .models import Playlist
from django_cron import CronJobBase, Schedule
from django.shortcuts import get_list_or_404, get_object_or_404
import io
from django.contrib.auth.decorators import login_required
import urllib, base64

import requests

max_client_id = '83403a77c90f4836b8287b70bac39a33'
max_client_secret = '48cd4347f180427fb116fd9376f10ca2'

client_credentials_manager = SpotifyClientCredentials(client_id=max_client_id,client_secret=max_client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def my_cron_job():
	print("CRON JOB GOING!")
	queryset = Playlist.objects.all()
	for playlist in queryset:
		playlist.followers_list += "," + str(sp.playlist(playlist.playlist_uri)['followers']['total'])
		now = datetime.now()
		playlist.dates_list += "," + now.strftime('%Y-%m-%d %H:%M:%S')
		playlist.save()
		print(playlist, playlist.followers_list)

@login_required
def home(request):
	if request.method == 'POST':
		ticker = request.POST.get("ticker")
		try:
			res = sp.playlist(ticker)
			pl = get_object_or_404(Playlist, playlist_uri=ticker)
			playlist_name = res['name']
			dates = [str(x)[:-3] for x in pl.dates_list.split(',') if x]
			folls = [int(x) for x in pl.followers_list.split(',') if x]
			image = res['images'][0]['url']
			len_headers = len(dates)
			len_data = len(folls)
			result = []
			for x in range(0, len_data, len_headers):
				for key, val in zip(dates, folls[x:x+len_headers]):
					result.append({'t': key, 'y': val})

			args = {'image': image, 'ticker': ticker, 'api' : res, 'playlist_name' : playlist_name, 'result': result}
			result = json.dumps(result)
			return render(request, 'home.html', args)
		except Exception as e:
			api = "Error..."
			logging.error(traceback.format_exc())
			return render(request, 'home.html', {'ticker': ticker, 'e' : e})

	else:


		return render(request, 'home.html', {'ticker': 'To get started, simply enter a spotify playlist URI into the search bar.'})

@login_required
def stock_added(request):
	if request.method == 'POST':
		ticker = request.POST['ticker']
		results = sp.playlist(ticker)
		now = datetime.now()
		new_playlist = Playlist(playlist_uri=ticker, followers_list=results['followers']['total'], dates_list=now.strftime('%Y-%m-%d %H:%M:%S'))
		new_playlist.save()
	return render(request, 'stock_added.html', {})

@login_required
def all_playlists(request):
	pls = Playlist.objects.all()

	return render(request, 'all_playlists.html', {'playlists' : pls})

@login_required
def add_stock(request):
	return render(request, 'add_stock.html', {})

@login_required
def compare_songs(request):
	return render(request, 'compare_songs.html', {})

@login_required
def view_songs(request):
    if request.method == 'POST':
        song1_features = sp.audio_features([request.POST['song1']])
        song2_features = sp.audio_features([request.POST['song2']])
        song1_name = sp.track(request.POST['song1'])['name']
        song2_name = sp.track(request.POST['song2'])['name']

    return render(request, 'view_songs.html', {'song1_features': song1_features[0], 'song2_features': song2_features[0], 'song1_name': song1_name, 'song2_name': song2_name})

@login_required
def view_recs(request):

    track_name = request.POST['track_name']
    recs = sp.recommendations(seed_tracks=[track_name])
    return render(request, 'view_recs.html', {'track_name' : track_name, 'recs' : recs})

@login_required
def get_recs(request):
    return render(request, 'get_recs.html', {})

@login_required
def about(request):
	return render(request, 'about.html', {})