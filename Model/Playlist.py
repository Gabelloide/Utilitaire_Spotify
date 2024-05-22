from typing import Dict, List
from Model import Artist, Track, Album, User

class Playlist:

	def __init__(self, playlistDict) -> None:
		self.collaborative: bool = playlistDict.get('collaborative')
		self.description: str = playlistDict.get('description')
		self.external_urls: dict = playlistDict.get('external_urls')
		self.followers: dict = playlistDict.get('followers')
		self.href: str = playlistDict.get('href')
		self.id: str = playlistDict.get('id')
		self.images: List[Dict[str, str]] = playlistDict.get('images', [])
		self.name: str = playlistDict.get('name')
		self.owner: User.User = None #TODO self.owner, a User object
		self.public: bool = playlistDict.get('public')
		# self.snapshot_id: str = playlistDict.get('snapshot_id') # Relevant ?
		self.uri: str = playlistDict.get('uri')

		# In case of playlists, tracks are nested in another dict containing added_at, added_by, is_local, primary_color, and the track itself after
		# self.tracks is thus a list of dictionaries
		self.tracks: List[Dict[str,str]] = playlistDict.get('tracks').get('items')
  
		# Modifying this dictionary to contain a Track object instead of a dictionary for the 'track' key
		self.tracks = [{'added_at': track['added_at'], 'added_by': track['added_by'], 'is_local': track['is_local'], 'primary_color': track['primary_color'], 'track': Track.Track(track['track'])} for track in self.tracks]


	def __str__(self) -> str:
		return self.name

	def getTracksObjects(self):
		"""Returns a list of Track objects ONLY, not the other keys in the dictionary."""
		return [track['track'] for track in self.tracks]

	def getTracksList(self):
		"""Returns a list of dictionaries containing the track object and additionnal keys."""
		return self.tracks