"""Django URLS"""

from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from . import views
from django.conf import settings

urlpatterns = [
    path('profile/<username>', views.user_profile, name='user_profile'),
	path('accounts/', include('django.contrib.auth.urls')),
	path('', views.home, name="home"),
	path('playlist/<int:pk>/', views.detail, name="playlist-detail"),
	path('<int:pk>/', views.detail, name="playlist-detail"),
	path('notready', views.not_ready, name="not_ready"),
	path('recs', views.get_recs, name="get_recs"),
	path('view_recs', views.view_recs, name="view_recs"),
	path('download_song', views.home, name="download_song"),
	path('compare', views.compare_songs, name="compare_songs"),
    path('view_songs', views.view_songs, name="view_songs"),
	path('about', views.about, name="about"),
	path('himom', views.himom, name="himom"),
	path('add', views.add_stock, name="add_stock"),
	path('playlist_success', views.stock_added, name="stock_added"),
	path('all', views.all_playlists, name="all_playlists"),
	path('playlist/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_playlist'),
	path('results', views.results, name="results"),
	path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
