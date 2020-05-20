from django.shortcuts import render
import requests
import json
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import traceback
import logging
from datetime import datetime
import getter
from .models import Playlist
from background_task import background
from django_cron import CronJobBase, Schedule
import io
from django.contrib.auth.decorators import login_required
import urllib, base64

import requests

max_client_id = '83403a77c90f4836b8287b70bac39a33'
max_client_secret = '48cd4347f180427fb116fd9376f10ca2'

client_credentials_manager = SpotifyClientCredentials(client_id=max_client_id,client_secret=max_client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
pg = getter.PlaylistGetter()
initial_playlists = ['spotify:playlist:0lxrR2ESnZjm8fPnaXODbv',
'spotify:playlist:0MMCB0rG70wSa2aLdxXidT',
'spotify:playlist:1FT2CwQxjkdFRtzOhNCyXh',
'spotify:playlist:1lWVabpPJSBoctR00myPHG',
'spotify:playlist:2HrIc0FQHCHSNJ21Q43lTy',
'spotify:playlist:2piahix4woQ9jkXK3iArNx',
'spotify:playlist:43udSsOeQC1mlUYf18fb2J',
'spotify:playlist:5e434MGaSp34Xp3goFo8Si',
'spotify:playlist:5S3lVGQRbqDSM8lNCKe2P7',
'spotify:playlist:7MCmRWuAkOM76ReXMdVGN4']
pg.track_all_playlists(initial_playlists)


@background(schedule=60)
def track_task():
	print("RUN BACKGROUND TEST!", pg.playlist_data)
	pg.track_all_playlists(initial_playlists)

@login_required
def home(request):


	if request.method == 'POST':
		pg.track_all_playlists(initial_playlists)
		ticker = request.POST.get("ticker")
		try:

			api = pg.playlist_data[ticker]
			percents = pg.get_playlist_percent_changes(ticker)
			percent_change = round(pg.get_percent_change(ticker), 3)
			first_num_followers = api['followers_data'][0]['followers']
			curr_num_followers = api['followers_data'][len(percents) - 1]['followers']
			change_in_followers = curr_num_followers - first_num_followers
			pg.graph(ticker)
			res = sp.playlist(ticker)
			image = res['images'][0]['url']
			args = {'image': image, 'ticker': ticker, 'api' : api, 'percents' : percents, 'percent_change' : percent_change, 'first_num_followers' : first_num_followers, 'curr_num_followers' : curr_num_followers, 'change_in_followers': change_in_followers}
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
		initial_playlists.append(request.POST['ticker'])
		pg.track_all_playlists(initial_playlists)
	return render(request, 'stock_added.html', {})

@login_required
def all_playlists(request):
	pls = []
	for pl in pg.playlist_data.keys():
	    api = pg.playlist_data[pl]
	    first_num_followers = api['followers_data'][0]['followers']
	    curr_num_followers = api['followers_data'][len(api['followers_data']) - 1]['followers']
	    percent_change = round(pg.get_percent_change(pl), 3)
	    diff = curr_num_followers - first_num_followers
	    datum = pg.playlist_data[pl]
	    pls.append((pl,datum,datum['followers_data'][-1]['followers'], diff, percent_change))

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
        song1_name = request.POST['song1name']
        song2_name = request.POST['song2name']

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