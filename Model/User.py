import Controller.SpotifyAPI as SpotifyAPI
from Model import Artist, Track
from typing import List

class User:

  def __init__(self, userDict) -> None:
    self.display_name	: str  = userDict.get('display_name')
    self.external_urls  : dict = userDict.get('external_urls', {})
    self.followers	    : dict = userDict.get('followers', {})
    self.href			: str  = userDict.get('href')
    self.id				: str  = userDict.get('id')
    self.images			: list = userDict.get('images', [])
    self.uri			: str  = userDict.get('uri')
    self.followers		: dict = userDict.get('followers', {})


  def __str__(self) -> str:
    return self.display_name
  
  
  def getTopArtists(self, client, limit=5) -> List[Artist.Artist]:
    results = client.current_user_top_artists(time_range='short_term') # 4 weeks
    items = results['items']
    # Filling the list with all the artists
    while results['next'] and len(items) < limit:
      results = client.next(results)
      items.extend(results['items'])
    
    # Creating Artist objects
    return [Artist.Artist(artist) for artist in items[:limit]]
  
  
  def getTopTracks(self, client, limit=5) -> List[Track.Track]:
    results = client.current_user_top_tracks(time_range='short_term') # 4 weeks
    items = results['items']
    # Filling the list with all the tracks
    while results['next'] and len(items) < limit: # If there are less than {limit} items, we need to fetch more
      results = client.next(results)
      items.extend(results['items'])

    # Creating Track objects
    return [Track.Track(track) for track in items[:limit]] # Limiting the number of tracks to {limit}


  def getBigProfilePicture(self):
    imageURL = None
    for image in self.images:
      if image['height'] == 300:
        imageURL = image['url']
    return imageURL
  

  def getTopAlbums(self):
    topTracks = self.getTopTracks(SpotifyAPI.get_spotify_client(), limit=150) # Limit will increase accuracy of score checking
    albumsScores = {}
    idAlbums = {}
    for track in topTracks:
      if track.album.album_type != 'SINGLE':
        albumsScores[track.album.id] = albumsScores.get(track.album.id, 0) + 1
        idAlbums[track.album.id] = track.album

    # Sorting the dictionary by values
    sortedAlbumsIDs = [k for k, v in sorted(albumsScores.items(), key=lambda item: item[1], reverse=True)]
    sortedAlbums = [idAlbums[albumID] for albumID in sortedAlbumsIDs]
    
    return sortedAlbums