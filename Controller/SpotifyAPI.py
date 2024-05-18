import spotipy

class SpotifyAPI:

  def __init__(self, client_id, client_secret, redirect_uri, scope):
    self.client_id = client_id
    self.client_secret = client_secret
    self.redirect_uri = redirect_uri
    self.scope = scope

  def get_spotify_client(self):
    """Gets the Spotify client object with the given credentials and scope."""
    return spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(client_id=self.client_id, client_secret=self.client_secret, redirect_uri=self.redirect_uri, scope=self.scope))
