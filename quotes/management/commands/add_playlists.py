from django.core.management.base import BaseCommand
from quotes.models import Playlist
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import os

MAX_CLIENT_ID = os.getenv("MAX_CLIENT_ID")
MAX_CLIENT_SECRET = os.getenv("MAX_CLIENT_SECRET")
client_credentials_manager = SpotifyClientCredentials(client_id=MAX_CLIENT_ID, client_secret=MAX_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

class Command(BaseCommand):
    help = 'add playlists'

    def handle(self, *args, **kwargs):
        uri_list = ['spotify:playlist:0c8wWuVXatnMhM3fvLo1sf',
                    'spotify:playlist:0fdqj4jwvfO0QZsU2iHwsH',
                    'spotify:playlist:0hk7OlJdg8W4fxRk0ZHpOI',
                    'spotify:playlist:178APKGN54qS1Utvaink7S',
                    'spotify:playlist:1ba2hqKlOPgO71nbN7VuQD',
                    'spotify:playlist:1d8TquHq728LoV2YzWMsNH',
                    'spotify:playlist:1l8uIKCRrd2FSzUlHmP8kA',
                    'spotify:playlist:1URIcSUOWfuKJibpv7fkpg',
                    'spotify:playlist:2ajvchwpQtCKqCOns59KME',
                    'spotify:playlist:2eKFAfOy2dhimLegWwUgr3',
                    'spotify:playlist:2hlVWHQPMevjFmsSpQ00Kf',
                    'spotify:playlist:2J0yk1YZbnuuhoCkC1EgWF',
                    'spotify:playlist:2RleBgemLa3352ScgVQ1Ul',
                    'spotify:playlist:2vodIR3v9nyJnj5AkQSCQ9',
                    'spotify:playlist:2xPwXX0Ny1lxsrPM3mEP01',
                    'spotify:playlist:3AkD2D1ei6Ha8RrRvNjdXe',
                    'spotify:playlist:3BNYuEzWgW3Vr6cEjxHZRT',
                    'spotify:playlist:3ftK0dIRDX5WpJ3d6zXJag',
                    'spotify:playlist:3jCSRTC3eqnZD3TYNi95Q6',
                    'spotify:playlist:3XtUu7oYDMg0Lyr52rBtvs',
                    'spotify:playlist:3zx6KxrEY8WNKTTIEpF8ZD',
                    'spotify:playlist:45ddEPvqtLYH6YIHDq4QvH',
                    'spotify:playlist:4A66799pR3SUz6nYrnDagO',
                    'spotify:playlist:4eoZFfyKKqXNRt1OQs3SbG',
                    'spotify:playlist:4Gpu2BiBp8QjHyX0IbvVLx',
                    'spotify:playlist:4IQbEfdg3RB63ILyGDjY1e',
                    'spotify:playlist:4tg8sxeB8CfQDdDaa3brhY',
                    'spotify:playlist:4WxLbK8aa2sA7qNwlySLms',
                    'spotify:playlist:5leXHB7CFPF55kUjY2zjIW',
                    'spotify:playlist:5lfvD9nXDAXEHPklaLP5OZ',
                    'spotify:playlist:5zjzkjr25IZhQifwe90MVA',
                    'spotify:playlist:6doFYo0Wk6DHvGZUBmhqnG',
                    'spotify:playlist:6KatOCMVmhcxr1AA5sYHlH',
                    'spotify:playlist:6nlx9ZF7MtxiosJxvz1ROE',
                    'spotify:playlist:6UBDajkcIX3VwizDIIecl1',
                    'spotify:playlist:6vbetH32Fk2oRjeznWkKtx',
                    'spotify:playlist:6YHBRPbW6QweuxRi4WDa0A',
                    'spotify:playlist:7aFQSN1KfyAxbcJs7WXgjQ',
                    'spotify:playlist:7BhTc0SC58ElfzvetwsEQh']
        for uri in uri_list:
            print(uri)
            results = sp.playlist(uri)
            new_playlist = Playlist(playlist_uri=uri, name=results['name'], sus=False)
            new_playlist.save()

