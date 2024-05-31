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
  recently_played_tracks = get_50_recently_played_tracks(client)
  total_duration = 0
  for track, played_at in recently_played_tracks.items():
    total_duration += track.duration_ms
  return total_duration


def get_50_recently_played_tracks(client):
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


def getRecentListeningGenres(client, limit=5):
  """Returns the top {limit} genres of the user's recent tracks."""
  recently_played_tracks = get_50_recently_played_tracks(client)
  genres_count = {}
  
  # Artists fetched from the creation of Track objects are not complete (no genre for instance), so we need to fetch them again
  # Using custom endpoint to fetch all the artists at once : https://api.spotify.com/v1/artists
  # This is much quicker than fetching each artist individually by the artist (singular) endpoint
  requestBase = "https://api.spotify.com/v1/artists?ids="
  
  ids = []
  for track in recently_played_tracks.keys():
    for artist in track.artists:
      ids.append(artist.id)
  
  # We must make batches of 50 artists per call to not exceed the api limit
  batchs = [ids[i:i+50] for i in range(0, len(ids), 50)] # a list of lists of artists ids, each list containing 50 artists max.
  
  for batch in batchs:
    requestURL = requestBase + ",".join(batch)
    response = client._get(requestURL)["artists"] # Fetching the artists
    fullArtists = [Artist(artist) for artist in response] # Creating Artist objects
    
    for fullArtist in fullArtists: # Filling the genres_count dictionary
      for genre in fullArtist.genres:
        genres_count[genre] = genres_count.get(genre, 0) + 1

  # Sorting the dictionary by values
  sorted_genres = sorted(genres_count.items(), key=lambda item: item[1], reverse=True)
  
  return sorted_genres[:limit]


def getNbPlayedTracks(client):
  return len(get_50_recently_played_tracks(client))


def getNbUniquePlayedTracks(client):
  tracks = get_50_recently_played_tracks(client)
  # Filtering on the ID
  uniqueTracks = []
  for track in tracks.keys():
    if track.id not in [t.id for t in uniqueTracks]:
      uniqueTracks.append(track)
  return len(uniqueTracks)


def getNbPlayedArtists(client):
  return len(getTopArtists(client)) # TODO : make artists come from the 50 most recently played tracks


def getNbUniquePlayedArtists(client):
  artists = getTopArtists(client) # TODO : make artists come from the 50 most recently played tracks
  # Filtering on the ID
  uniqueArtists = []
  for artist in artists:
    if artist.id not in [a.id for a in uniqueArtists]:
      uniqueArtists.append(artist)
  return len(uniqueArtists)


def getNbPlayedAlbums(client):
  return len(getTopAlbums(client)) # TODO : make albums come from the 50 most recently played tracks