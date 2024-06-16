from typing import List, Dict
from Model import Artist, Album

class Track:
  
  tracks_genres_cache = {} # Cache : key is track id, value is genre list
  
  def __init__(self, track_dict: Dict):
    self.album            : Album.Album = Album.Album(track_dict.get('album', {}))
    self.artists          : list = [Artist.Artist(artist) for artist in track_dict.get('artists', [])]
    self.disc_number      : int = track_dict.get('disc_number')
    self.duration_ms      : int = track_dict.get('duration_ms')
    self.explicit         : bool= track_dict.get('explicit')
    self.external_ids     : dict = track_dict.get('external_ids', {})
    self.external_urls    : dict = track_dict.get('external_urls', {})
    self.href             : str = track_dict.get('href')
    self.id               : str = track_dict.get('id')
    self.is_local         : bool = track_dict.get('is_local')
    self.is_playable      : bool = track_dict.get('is_playable')
    self.name             : str = track_dict.get('name')
    self.popularity       : int = track_dict.get('popularity')
    self.preview_url      : str = track_dict.get('preview_url')
    self.track_number     : int = track_dict.get('track_number')
    self.uri              : str = track_dict.get('uri')

  def __str__(self) -> str:
    string = f"{self.name} by"
    for artist in self.artists:
      string += f" {artist},"
    string = string[:-1]
    return string
  

  def get_track_genre(self, client):
    """Function to get the genre of a track"""
    if self.id in Track.tracks_genres_cache:
      print(f"Returning cached genre for {self.id}.")
      return Track.tracks_genres_cache[self.id]
    
    # Get the artist ID from the track object
    artist_id = self.artists[0].id
    # Get the artist object using the artist ID
    artist = client.artist(artist_id)
    # Get the genre from the artist object
    genre = artist['genres']

    Track.tracks_genres_cache[self.id] = genre
    return genre
