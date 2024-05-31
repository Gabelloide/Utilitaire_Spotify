from Model.Album import Album
from Model.Artist import Artist
from Model.Track import Track
from Model.User import User
from Model.Playlist import Playlist

from datetime import datetime, timedelta

def getListeningDuration(client, time_range="short_term"):
  if time_range not in ['short_term', 'medium_term', 'long_term']:
    raise ValueError("time_range must be one of 'short_term', 'medium_term', 'long_term'")
  
  # Get the current date
  current_date = datetime.date.today()
  
  if time_range == 'short_term':
    # Calculate the date four weeks before today
    start_date = current_date - datetime.timedelta(weeks=4)
  elif time_range == 'medium_term':
    # Calculate the date six months before today
    start_date = current_date - datetime.timedelta(weeks=26)
  else:
    # Calculate the date one year before today
    start_date = current_date - datetime.timedelta(weeks=52)
  
  # Use the start_date to fetch the recently played tracks
  recently_played_tracks = client.current_user_recently_played(after=start_date) # TODO FIX : le truc avec le after
  
  # Tracks are inside items key
  # One item is a dict containing three keys : track, played_at, context
  recently_played_tracks = recently_played_tracks['items']
  
  # Create a dictionary with track objects as keys and played_at as values
  recently_played_tracks = {Track(track['track']): track['played_at'] for track in recently_played_tracks}
  
  listening_duration = sum([track.duration for track in recently_played_tracks.keys()])
  
  # Return the listening duration
  return listening_duration