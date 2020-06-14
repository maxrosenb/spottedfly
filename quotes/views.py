"""
Spottedfly views.py
"""
import json
import traceback
import logging
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from .models import Playlist
from .forms import CommentForm
MAX_CLIENT_ID = '83403a77c90f4836b8287b70bac39a33'
MAX_CLIENT_SECRET = '48cd4347f180427fb116fd9376f10ca2'

client_credentials_manager = SpotifyClientCredentials(client_id=MAX_CLIENT_ID, client_secret=MAX_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_client_ip(request):
	"""get client ip"""
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip

def my_cron_job():
	"""Cron Job to Refresh Playlist Followers Info"""
	print("CRON JOB GOING!")
	queryset = Playlist.objects.all()
	for playlist in queryset:
		playlist.followers_list += "," + str(sp.playlist(playlist.playlist_uri)['followers']['total'])
		now = datetime.now()
		playlist.dates_list += "," + now.strftime('%Y-%m-%d %H:%M:%S')
		playlist.save()
		print(playlist, playlist.followers_list)

def home(request):
    print(get_client_ip(request), " visited the home page")
    """Displays Home Page"""
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
    		playlist = Playlist.objects.get(playlist_uri=ticker)
    		for x in range(0, len_data, len_headers):
    			for key, val in zip(dates, folls[x:x+len_headers]):
    				result.append({'t': key, 'y': val})
			#print(get_client_ip(request), "accessed a chart")
    		args = {'image': image, 'ticker': ticker, 'api' : res, 'playlist_name' : playlist_name, 'result': result, 'init_followers' : folls[0], 'playlist' : playlist}
    		result = json.dumps(result)
    		return render(request, 'home.html', args)
    	except ValueError as e_error:
    		print(e_error)
    		logging.error(traceback.format_exc())
    		return render(request, 'home.html', {'ticker': ticker, 'e' : 'The requested playlist is not ready yet, just check back after the hour and get data mining.'})
    else:
    	return redirect(all_playlists)

@login_required
def stock_added(request):
	"""Page Displayed After Adding Playlist"""
	users_in_group = Group.objects.get(name="can_add").user_set.all()
	if request.user in users_in_group:

	    if request.method == 'POST':
		    ticker = request.POST['ticker']
		    results = sp.playlist(ticker)
		    new_playlist = Playlist(playlist_uri=ticker, name=results['name'], sus=False)
		    new_playlist.save()
	    return redirect(all_playlists)
	else:
	    raise PermissionDenied

def all_playlists(request):
	"""View List of Playlist"""
	pls = Playlist.objects.order_by("pk").reverse()
	paginator = Paginator(pls, 10) # Show 25 contacts per page.
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	return render(request, 'all_playlists.html', {'playlists' : pls, 'page_obj': page_obj})

def add_stock(request):
	"""Add a Playlist"""
	users_in_group = Group.objects.get(name="can_add").user_set.all()
	if request.user in users_in_group:
	    return render(request, 'add_stock.html', {})
	else:
	    raise PermissionDenied

def compare_songs(request):
	"""Compare Two Songs"""
	return render(request, 'compare_songs.html', {})

def view_songs(request):
	"""View The Two Compared Songs"""
	if request.method == 'POST':
		song1_features = sp.audio_features([request.POST['song1']])
		song2_features = sp.audio_features([request.POST['song2']])
		song1_name = sp.track(request.POST['song1'])['name']
		song2_name = sp.track(request.POST['song2'])['name']

	return render(request, 'view_songs.html', {'song1_features': song1_features[0], 'song2_features': song2_features[0], 'song1_name': song1_name, 'song2_name': song2_name})

def view_recs(request):
	"""View Track Recommendations"""

	track_name = request.POST['track_name']
	recs = sp.recommendations(seed_tracks=[track_name])
	return render(request, 'view_recs.html', {'track_name' : track_name, 'recs' : recs})

def get_recs(request):
	"""Get Track Recommendations"""
	return render(request, 'get_recs.html', {})

def about(request):
	"""About"""
	return render(request, 'about.html', {})

def add_comment_to_post(request, pk):
	""" Add Comment to Playlist """
	post = get_object_or_404(Playlist, pk=pk)
	if request.method == "POST":
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post
			comment.save()
			return redirect(all_playlists)
	else:
		form = CommentForm()
	return render(request, 'add_comment_to_playlist.html', {'form': form})

def publickey(request):
    return render(request, 'publickey.html', {})

def privatekey(request):
    return render(request, 'privatekey.html', {})

