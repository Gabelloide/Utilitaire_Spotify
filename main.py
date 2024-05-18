import os
import Controller.SpotifyAPI as SpotifyAPI
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

user = spotipy_client.current_user()
print(user)
