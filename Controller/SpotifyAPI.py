import spotipy
import os

spotify_client = None

# Variables filled at startup & refresh to prevent multiple calls to the API
# If we are saving calls in a dictionary, the key is the parameters that were used to get the data, the value is the data itself
recently_played_tracks_cache = None
recently_played_artists_cache = None
recently_played_albums_cache = None
top_artists_cache = {}
top_tracks_cache = {}
top_albums_cache = {}
recent_listening_genres_cache = {}


def setup_client(client_id, client_secret, redirect_uri, scope):
  global spotify_client
  spotify_client = spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))

def get_spotify_client():
  """Gets the Spotify client object with the given credentials and scope."""
  return spotify_client

def getClientParameters():
  client_id = os.getenv('SPOTIPY_CLIENT_ID')
  client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
  redirect_uri = "http://localhost:12345" # Must match this address (registered in the Spotify Developer Dashboard)
  scopes = "user-library-read user-read-private user-read-email user-read-playback-state user-modify-playback-state user-read-currently-playing user-read-recently-played user-top-read"
  return client_id, client_secret, redirect_uri, scopes