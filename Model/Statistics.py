from Model.Album import Album
from Model.Artist import Artist
from Model.Track import Track
from Model.User import User
from Model.Playlist import Playlist


def getListeningDuration(client, time_range="short_term"):
  if time_range not in ['short_term', 'medium_term', 'long_term']:
    raise ValueError("time_range must be one of 'short_term', 'medium_term', 'long_term'")