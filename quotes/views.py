"""
Spottedfly views.py
"""
import json
import traceback
import logging
import os
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from .models import Playlist, User
from .forms import CommentForm
MAX_CLIENT_ID = os.getenv("MAX_CLIENT_ID")
MAX_CLIENT_SECRET = os.getenv("MAX_CLIENT_SECRET")

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
    """Displays Home Page"""
    if get_client_ip(request) != "24.20.48.43":
        print(get_client_ip(request), " visited the home page")

    return redirect(all_playlists)


def detail(request,pk):
    pl_result = Playlist.objects.get(pk=pk)
    dates = [str(x)[:-3] for x in pl_result.dates_list.split(',') if x]
    folls = [int(x) for x in pl_result.followers_list.split(',') if x != "None"]
    #image is the last field needed to be saved to the database before we can stop making API calls in this view
    len_headers = len(dates)
    len_data = len(folls)
    if len_headers == 0:
        return redirect('/notready')
    result = []
    for x in range(0, len_data, len_headers):
    	for key, val in zip(dates, folls[x:x+len_headers]):
    		result.append({'t': key, 'y': val})
	#print(get_client_ip(request), "accessed a chart")
    link = "https://open.spotify.com/playlist/" + pl_result.playlist_uri[17:]
    xframe_uri = pl_result.playlist_uri[17:]
    rgb_red = pl_result.photo_red
    rgb_green = pl_result.photo_green
    rgb_blue = pl_result.photo_blue
    args = {'rgb_red': rgb_red, 'rgb_green': rgb_green, 'rgb_blue': rgb_blue, 'xframe_uri': xframe_uri, 'link': link, 'ticker': pl_result.playlist_uri, 'result': result, 'init_followers' : folls[0],'latest_followers' : folls[-1:][0], 'playlist' : pl_result}
    return render(request, 'detail.html', args)

def not_ready(request):
    return render(request, 'not_ready.html', {})

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
	paginator = Paginator(pls, 20) # Show 20 playlists per page.
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	return render(request, 'all_playlists.html', {'playlists' : pls, 'page_obj': page_obj})

def results(request):
	"""View List of Playlist"""
	ticker = request.POST.get("ticker")
	pls = Playlist.objects.filter(tags__name__in=[ticker]) | Playlist.objects.filter(name__contains=ticker)
	paginator = Paginator(pls, 10) # Show 25 contacts per page.
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	return render(request, 'results.html', {'playlists' : pls, 'page_obj': page_obj})

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
			comment.author = request.user
			comment.save()
			return redirect(all_playlists)
	else:
		form = CommentForm()
	return render(request, 'add_comment_to_playlist.html', {'form': form})

def publickey(request):
    return render(request, 'publickey.html', {})

def privatekey(request):
    return render(request, 'privatekey.html', {})

def himom(request):
    return render(request, 'himom.html', {})

def user_profile(request, username):
    user = User.objects.get(username=username)
    context = {
       "user": user
    }
    return render(request, 'user_profile.html', context)
