from datetime import datetime
import time
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import json
import os

matplotlib.use('Agg')
client_credentials_manager = SpotifyClientCredentials(client_id='83403a77c90f4836b8287b70bac39a33',client_secret="48cd4347f180427fb116fd9376f10ca2")
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

class PlaylistGetter:
    def __init__(self):
        self.playlist_data = {}

    def track(self, uri):

        results = sp.playlist(uri)
        now = datetime.now()
        followers = results['followers']['total']
        name = results['name']

        if uri in self.playlist_data.keys():
            self.playlist_data[uri]['followers_data'].append({'timestamp' : now,'followers': followers})
        else:
            self.playlist_data[uri] = { 'name' : name, 'followers_data': [{'timestamp' : now, 'followers': followers}]}

    def get_data_from_file(self, csvfile):
        with open(csvfile) as f:
            json_data = json.load(f)
        for key in json_data.keys():
            self.playlist_data[key] = { 'name' : json_data[key]['name'], 'followers_data' :json_data[key]['followers_data']}


    def save_all_data_to_txt(self):
        with open('data.txt', 'w') as outfile:
            json.dump(self.playlist_data, outfile, indent=4, sort_keys=True, default=str)

    def track_all_playlists(self, plists):
        print("Running track all playlists")
        self.get_data_from_file
        for playlist in plists:
            self.track(playlist)
        self.save_all_data_to_txt()

    def get_percent_change(self, uri):
        followers_data = self.playlist_data[uri]['followers_data']
        return 100 * abs(1 - (followers_data[len(followers_data)-1]['followers'] / followers_data[0]['followers']))


    def get_playlist_percent_changes(self, uri):
        followers = self.playlist_data[uri]['followers_data']
        res = [0]
        for i in range(1, len(followers)):
            res.append(100 * abs(1 - (followers[i]['followers'] / followers[0]['followers'])))
        return res

    def graph(self, uri):
        data =  self.playlist_data[uri]
        y_vars = self.get_playlist_percent_changes(uri)
        print(type(data['followers_data'][0]['timestamp']))
        x_vars = [datapoint['timestamp'] for datapoint in data['followers_data']]
        graph_name = data['name']

        fig, ax = plt.subplots(1)
        fig.autofmt_xdate()
        fig.patch.set_facecolor('#28A745')
        #ax.set_facecolor("m")
        plt.title(graph_name[:20] + " Follower Growth")
        plt.xlabel('Time')
        plt.ylabel('Spotify Followers Gained (%)')
        plt.plot(x_vars, y_vars, 'ko-', label=data['name'])
        plt.tight_layout()
        my_path = '/home/maxrosenbe/spottedflyweb/'
        fig.savefig(my_path + 'static/stocks/graph.png', facecolor = fig.get_facecolor(), dpi=130)


if __name__ == "__main__":
    playlists = ['spotify:playlist:7dxjMUob42LjvS9uNkcdl4',
                'spotify:playlist:1kuvKUsWFvzELdUQn94XxY',
                'spotify:playlist:6GiFeACBNcDux53vzTqjwj',
                'spotify:playlist:1Me5JiRrpe9MmZiH2XzP0C',
                'spotify:playlist:7q0i2c5CmnXpjP5LfyVIj3',
                'spotify:playlist:40bEHNh0CRn9lKjShMSFLD']

    pg = PlaylistGetter()
    #pg.track_all_playlists(playlists)
    #pg.track_on_loop(playlists)
    #pg.get_data_from_file('data.txt')
    #print(pg.get_playlist_data('spotify:playlist:7dxjMUob42LjvS9uNkcdl4')['followers'][0])
