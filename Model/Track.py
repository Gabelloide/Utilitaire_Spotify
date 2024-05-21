from typing import List, Dict
import Model.Artist as Artist

class Track:
	def __init__(self, track_dict: Dict):
		self.album = track_dict['album']['name'] #TODO Album object
		self.artists: list = [Artist.Artist(artist) for artist in track_dict['artists']]
		self.disc_number: int = track_dict['disc_number']
		self.duration_ms: int = track_dict['duration_ms']
		self.explicit: bool= track_dict['explicit']
		self.external_ids: dict = track_dict['external_ids']
		self.external_urls: dict = track_dict['external_urls']
		self.href: str = track_dict['href']
		self.id: str = track_dict['id']
		self.is_local: bool = track_dict['is_local']
		self.is_playable: bool = track_dict['is_playable']
		self.name: str = track_dict['name']
		self.popularity: int = track_dict['popularity']
		self.preview_url: str = track_dict['preview_url']
		self.track_number: int = track_dict['track_number']
		self.uri: str = track_dict['uri']
  
	def __str__(self) -> str:
		string = f"{self.name} by"
		for artist in self.artists:
			string += f" {artist},"
		string = string[:-1]
		return string
