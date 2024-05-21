from typing import List, Dict

class Artist:
	def __init__(self, artistDict) -> None:
		"""The artistDict is composed of nested dictionaries that contains the artist's information
		external_urls, followers, genres, href, id, images, name, popularity, type, uri."""
		self.external_urls: dict = artistDict.get('external_urls')
		self.followers: dict = artistDict.get('followers')
		self.genres:list = artistDict.get('genres')
		self.href:str = artistDict.get('href')
		self.id = artistDict.get('id')
		self.images: List[Dict[str, str]] = artistDict.get('images')
		self.name: str = artistDict.get('name')
		self.popularity: int = artistDict.get('popularity')
		self.uri:str = artistDict.get('uri') # Spotify URI for the artist


	def __str__(self) -> str:
		return self.name


	def getTotalFollowers(self):
		return self.followers['total']