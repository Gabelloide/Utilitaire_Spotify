from Model.Album import Album
from Model.Artist import Artist
from Model.Track import Track
from Model.User import User
from Model.Playlist import Playlist

from typing import List

# This module is responsible for getting the statistics of the user.
# Theses statistics are those made wihout any imported data
# For recent tracks, this means a maximum of 50 tracks.

def getRecentListeningDuration(client):
  """Will get the total listening duration (ms) of the user in the last 50 tracks."""
  recently_played_tracks = get_50_recently_played(client)
  total_duration = 0
  for track, played_at in recently_played_tracks.items():
    total_duration += track.duration_ms
  return total_duration


def get_50_recently_played(client):
  """Returns a dictionary containing the 50 most recently played tracks associated with their played_at date."""
  recently_played_tracks = client.current_user_recently_played()
  recently_played_tracks = recently_played_tracks['items']
  recently_played_dict = {Track(track['track']): track['played_at'] for track in recently_played_tracks}
  return recently_played_dict


def getTopArtists(client, limit=5, time_range="short_term") -> List[Artist]:
  """Returns the top {limit} artists of the user in the last {time_range}."""
  if time_range not in ['short_term', 'medium_term', 'long_term']:
    raise ValueError("Time range must be 'short_term', 'medium_term' or 'long_term'.")
  results = client.current_user_top_artists(time_range=time_range) # 4 weeks
  items = results['items']
  # Filling the list with all the artists
  while results['next'] and len(items) < limit:
    results = client.next(results)
    items.extend(results['items'])
  
  # Creating Artist objects
  return [Artist(artist) for artist in items[:limit]]


def getTopTracks(client, limit=5, time_range="short_term") -> List[Track]:
  """Returns the top {limit} tracks of the user in the last {time_range}."""
  if time_range not in ['short_term', 'medium_term', 'long_term']:
    raise ValueError("Time range must be 'short_term', 'medium_term' or 'long_term'.")
  results = client.current_user_top_tracks(time_range=time_range) # 4 weeks
  items = results['items']
  # Filling the list with all the tracks
  while results['next'] and len(items) < limit: # If there are less than {limit} items, we need to fetch more
    results = client.next(results)
    items.extend(results['items'])

  # Creating Track objects
  return [Track(track) for track in items[:limit]] # Limiting the number of tracks to {limit}


def getTopAlbums(client, limit=5, time_range="short_term") -> List[Album]:
  """Returns the top {limit} albums of the user in the last {time_range}."""
  if time_range not in ['short_term', 'medium_term', 'long_term']:
    raise ValueError("Time range must be 'short_term', 'medium_term' or 'long_term'.")
  topTracks = getTopTracks(client, limit=150, time_range=time_range) # Limit will increase accuracy of score checking
  albumsScores = {}
  idAlbums = {}
  for track in topTracks:
    if track.album.album_type != 'SINGLE':
      albumsScores[track.album.id] = albumsScores.get(track.album.id, 0) + 1
      idAlbums[track.album.id] = track.album

  # Sorting the dictionary by values
  sortedAlbumsIDs = [k for k, v in sorted(albumsScores.items(), key=lambda item: item[1], reverse=True)]
  sortedAlbums = [idAlbums[albumID] for albumID in sortedAlbumsIDs][:limit]
  
  return sortedAlbums


def getNbPlayedTracks():
  return len(get_50_recently_played())


def getNbPlayedArtists():
  return len(getTopArtists())


def getNbPlayedAlbums():
  return len(getTopAlbums())