import spotipy

spotify_client = None

def setup_client(client_id, client_secret, redirect_uri, scope):
  global spotify_client
  spotify_client = spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))

def get_spotify_client():
  """Gets the Spotify client object with the given credentials and scope."""
  return spotify_client