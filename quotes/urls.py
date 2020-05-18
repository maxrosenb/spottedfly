from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name="home"),
	path('about', views.about, name="about"),
	path('add', views.add_stock, name="add_stock"),
	path('playlist_success', views.stock_added, name="stock_added"),
	path('all', views.all_playlists, name ="all_playlists")
]
