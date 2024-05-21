import os
import Controller.SpotifyAPI as SpotifyAPI
import Model.Artist as Artist
import Model.Track as Track
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

for key, value in tracks[0].items():
		print(f"{key}: {value}")