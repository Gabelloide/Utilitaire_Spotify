from Model.Album import Album
from Model.Artist import Artist
from Model.Track import Track
from Model.User import User
from Model.Playlist import Playlist
from Controller import SpotifyAPI

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
  if SpotifyAPI.recently_played_tracks_cache is not None:
    print("Returning cached tracks.")
    return SpotifyAPI.recently_played_tracks_cache

  recently_played_tracks = client.current_user_recently_played()
  recently_played_tracks = recently_played_tracks['items']
  recently_played_dict = {Track(track['track']): track['played_at'] for track in recently_played_tracks}
  
  SpotifyAPI.recently_played_tracks_cache = recently_played_dict
  return recently_played_dict


def get_recently_played_artists(client):
  """Returns a list of Artist objects present in the 50 most recently played tracks.
  If an artist is present multiple times, it will only be counted once."""
  if SpotifyAPI.recently_played_artists_cache is not None:
    print("Returning cached artists.")
    return SpotifyAPI.recently_played_artists_cache
  
  recently_played_dict = get_50_recently_played_tracks(client)
  artists = []
  for track in recently_played_dict.keys():
    for artist in track.artists:
      # Before adding, check if artist id is already in the list
      if artist.id not in [a.id for a in artists]:
        artists.append(artist)

  SpotifyAPI.recently_played_artists_cache = artists
  return artists


def get_recently_played_albums(client):
  """Returns a list of Album objects present in the 50 most recently played tracks.
  If an album is present multiple times, it will only be counted once."""
  if SpotifyAPI.recently_played_albums_cache is not None:
    print("Returning cached albums.")
    return SpotifyAPI.recently_played_albums_cache
  
  recently_played_dict = get_50_recently_played_tracks(client)
  albums = []
  for track in recently_played_dict.keys():
    # Before adding, check if album id is already in the list
    if track.album.id not in [a.id for a in albums]:
      albums.append(track.album)
  
  SpotifyAPI.recently_played_albums_cache = albums
  return albums


def getTopArtists(client, limit=5, time_range="short_term") -> List[Artist]:
  """Returns the top {limit} artists of the user in the last {time_range}."""
  parameters = (limit, time_range)
  if parameters in SpotifyAPI.top_artists_cache :
    print("Returning cached top artists.")
    return SpotifyAPI.top_artists_cache[parameters]
  
  if time_range not in ['short_term', 'medium_term', 'long_term']:
    raise ValueError("Time range must be 'short_term', 'medium_term' or 'long_term'.")
  results = client.current_user_top_artists(time_range=time_range) # 4 weeks
  items = results['items']
  # Filling the list with all the artists
  while results['next'] and len(items) < limit:
    results = client.next(results)
    items.extend(results['items'])
  
  # Caching results
  topArtists = [Artist(artist) for artist in items[:limit]]
  SpotifyAPI.top_artists_cache[parameters] = topArtists
  return topArtists


def getTopTracks(client, limit=5, time_range="short_term") -> List[Track]:
  """Returns the top {limit} tracks of the user in the last {time_range}."""
  parameters = (limit, time_range)
  if parameters in SpotifyAPI.top_tracks_cache :
    print("Returning cached top tracks.")
    return SpotifyAPI.top_tracks_cache[parameters]
  
  if time_range not in ['short_term', 'medium_term', 'long_term']:
    raise ValueError("Time range must be 'short_term', 'medium_term' or 'long_term'.")
  results = client.current_user_top_tracks(time_range=time_range) # 4 weeks
  items = results['items']
  # Filling the list with all the tracks
  while results['next'] and len(items) < limit: # If there are less than {limit} items, we need to fetch more
    results = client.next(results)
    items.extend(results['items'])

  # Caching results
  topTracks = [Track(track) for track in items[:limit]] # Limiting the number of tracks to {limit}
  SpotifyAPI.top_tracks_cache[parameters] = topTracks
  return topTracks


def getTopAlbums(client, limit=5, time_range="short_term") -> List[Album]:
  """Returns the top {limit} albums of the user in the last {time_range}."""
  parameters = (limit, time_range)
  if parameters in SpotifyAPI.top_albums_cache :
    print("Returning cached top albums.")
    return SpotifyAPI.top_albums_cache[parameters]
  
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
  
  SpotifyAPI.top_albums_cache[parameters] = sortedAlbums
  return sortedAlbums


def getRecentListeningGenres(client, limit=5):
  """Returns the top {limit} genres of the user's recent tracks."""
  parameters = limit
  if parameters in SpotifyAPI.recent_listening_genres_cache:
    print("Returning cached genres.")
    return SpotifyAPI.recent_listening_genres_cache[parameters]
  
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
  
  genres = sorted_genres[:limit]
  SpotifyAPI.recent_listening_genres_cache[parameters] = genres
  return genres


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
  return len(get_recently_played_artists(client))


def getNbPlayedAlbums(client):
  return len(get_recently_played_albums(client))