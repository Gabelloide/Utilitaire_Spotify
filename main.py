import os
from pprint import pprint
import utils

import Controller.SpotifyAPI as SpotifyAPI
from Model import Artist, Track, Album, Playlist, User
from Controller import ControllerLogin
from Controller import MainWindow

from PyQt6.QtWidgets import QApplication



# --- Load environment variables ---
utils.load_env()

# --- Spotify API connection ---

client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
redirect_uri = "http://localhost:12345" # Must match this address (registered in the Spotify Developer Dashboard)

# It is possible to accumulate scopes by separating them with a space (temporary solution for test purposes)
scopes = "user-library-read user-read-private user-read-email user-read-playback-state user-modify-playback-state user-read-currently-playing user-read-recently-played user-top-read"


SpotifyAPI.setup_client(client_id, client_secret, redirect_uri, scopes)
spotipy_client = SpotifyAPI.get_spotify_client()

# --- Tests ---

# artistLink = 'https://open.spotify.com/artist/7LTiBdByoaUd329wCpmMcM?si=5ad5ee3bae52486a'

# Get artist from link
# artist = spotipy_client.artist(artistLink)
# maisondes = Artist.Artist(artist)

# tracks = spotipy_client.artist_top_tracks(maisondes.id)
# Unpack the dictionary into a list of tracks
# tracks = [track for track in tracks['tracks']]


# for key, value in tracks[0].items():
# 		print(f"{key}: {value}")
  
  
# Get album from URI
# albumURL = "https://open.spotify.com/album/0max2UoPzegnhjwv1yhyEC?si=yNdgtWk2Q82ciBAnpdWNUw"

# albumDict = spotipy_client.album(albumURL)
# album = Album.Album(albumDict)


# artists = [artist.name for artist in album.artists]
# tracks = [track.name for track in album.getTracks()]
# pprint(tracks)
# pprint(artists)

# playlistURL = "https://open.spotify.com/playlist/3JZ3gyqqGjbZ7zi04UuXNf?si=9aa70fd703584c48"

# playlistDict = spotipy_client.playlist(playlistURL)
# playlist = Playlist.Playlist(playlistDict)

# --- TEST : remplissage de la playlist. La playlist est limitée à 100 tracks lors de son instanciation, mais on peut la remplir entièrement avec la méthode fillPlaylist() ---
# print(len(playlist.getTracksList()))
# playlist.fillPlaylist()
# print(len(playlist.getTracksList()))

# print(vars(playlist.owner))
# ---------------------------------------------

# unetrack = playlistDict['tracks']["items"][0]

# for key, value in unetrack.items():
# 		print(f"{key}: {value}\n\n\n")

# cpt = 0
# for elt in playlist.getTracksList():
# 	print(elt)
# 	print()
# 	cpt += 1
# 	if cpt == 10:
# 		break

# user = User.User(spotipy_client.current_user())

# lis = spotipy_client.current_user_recently_played()

# tracks = [Track.Track(track['track']) for track in lis['items']]

# # pprint([track.name for track in tracks])

# searchResult = spotipy_client.search(q='Maison des', type='track', limit=1)
# pprint(searchResult)

# user = User.User(spotipy_client.current_user())
# tracksNames = [track.name for track in user.getTopTracks(spotipy_client)]
# pprint(len(tracksNames))
# artistsNames = [artist.name for artist in user.getTopArtists(spotipy_client)]
# pprint(artistsNames)

# topAlbumsNames = [album.name for album in user.getTopAlbums()]
# pprint(topAlbumsNames)


# track = Track.Track(spotipy_client.current_user_recently_played()['items'][0]['track'])

# --- GUI ---

# app = QApplication([])
# window = MainWindow.MainWindow()
# window.show()
# app.exec()