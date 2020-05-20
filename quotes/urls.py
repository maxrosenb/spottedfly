from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('login', LoginView.as_view()),
	path('', views.home, name="home"),
	path('recs', views.get_recs, name="get_recs"),
	path('view_recs', views.view_recs, name="view_recs"),
	path('download_song', views.home, name="download_song"),
	path('compare', views.compare_songs, name="compare_songs"),
    path('view_songs', views.view_songs, name="view_songs"),
	path('about', views.about, name="about"),
	path('add', views.add_stock, name="add_stock"),
	path('playlist_success', views.stock_added, name="stock_added"),
	path('all', views.all_playlists, name ="all_playlists")
]
