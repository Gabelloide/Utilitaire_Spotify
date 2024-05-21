from typing import List, Dict

class Artist():
	def __init__(self, artistDict) -> None:
		"""The artistDict is composed of nested dictionaries that contains the artist's information
		external_urls, followers, genres, href, id, images, name, popularity, type, uri."""

		self.external_urls: dict = artistDict['external_urls']
		self.followers: dict = artistDict['followers']
		self.genres:list = artistDict['genres']
		self.href:str = artistDict['href']
		self.id = artistDict['id']
		self.images: List[Dict[str, str]] = artistDict['images']
		self.name: str = artistDict['name']
		self.popularity: int = artistDict['popularity']
		self.uri:str = artistDict['uri'] # Spotify URI for the artist


	def __str__(self) -> str:
		return self.name


	def getTotalFollowers(self):
		return self.followers['total']