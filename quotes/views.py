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

client_credentials_manager = SpotifyClientCredentials(client_id='83403a77c90f4836b8287b70bac39a33',client_secret="48cd4347f180427fb116fd9376f10ca2")
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
pg = getter.PlaylistGetter()
initial_playlists = ['spotify:playlist:7dxjMUob42LjvS9uNkcdl4',
                'spotify:playlist:1kuvKUsWFvzELdUQn94XxY',
                'spotify:playlist:6GiFeACBNcDux53vzTqjwj',
                'spotify:playlist:1Me5JiRrpe9MmZiH2XzP0C',
                'spotify:playlist:7q0i2c5CmnXpjP5LfyVIj3',
                'spotify:playlist:40bEHNh0CRn9lKjShMSFLD']
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
		datum = pg.playlist_data[pl]
		pls.append((pl,datum,datum['followers_data'][-1]['followers']))

	return render(request, 'all_playlists.html', {'playlists' : pls})

@login_required
def add_stock(request):
	return render(request, 'add_stock.html', {})

@login_required
def about(request):
	return render(request, 'about.html', {})