import os
from pprint import pprint

import Controller.SpotifyAPI as SpotifyAPI
from Model import Artist, Track, Album, Playlist
import utils


# --- Load environment variables ---
utils.load_env()

# --- Spotify API connection ---

client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
redirect_uri = "http://localhost:12345" # Must match this address (registered in the Spotify Developer Dashboard)

# It is possible to accumulate scopes by separating them with a space (temporary solution for test purposes)
scope = "user-library-read user-read-private user-read-email user-read-playback-state user-modify-playback-state user-read-currently-playing"

api = SpotifyAPI.SpotifyAPI(client_id, client_secret, redirect_uri, scope)
spotipy_client = api.get_spotify_client()

# --- Tests ---

artistLink = 'https://open.spotify.com/artist/7LTiBdByoaUd329wCpmMcM?si=5ad5ee3bae52486a'

# Get artist from link
artist = spotipy_client.artist(artistLink)
maisondes = Artist.Artist(artist)

tracks = spotipy_client.artist_top_tracks(maisondes.id)
# Unpack the dictionary into a list of tracks
tracks = [track for track in tracks['tracks']]


# for key, value in tracks[0].items():
# 		print(f"{key}: {value}")
  
  
# Get album from URI
albumURL = "https://open.spotify.com/album/0max2UoPzegnhjwv1yhyEC?si=yNdgtWk2Q82ciBAnpdWNUw"

albumDict = spotipy_client.album(albumURL)
album = Album.Album(albumDict)


artists = [artist.name for artist in album.artists]
tracks = [track.name for track in album.getTracks()]
# pprint(tracks)
# pprint(artists)

playlistURL = "https://open.spotify.com/playlist/3JZ3gyqqGjbZ7zi04UuXNf?si=9aa70fd703584c48"

playlistDict = spotipy_client.playlist(playlistURL)
playlist = Playlist.Playlist(playlistDict)

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
