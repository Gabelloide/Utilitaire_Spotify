import Artist, Track

class Album:

	def __init__(self, album_dict):
		self.album_type: str = album_dict.get('album_type')
		self.artists: list[Artist.Artist] = [Artist.Artist(artist) for artist in album_dict.get('artists', [])]
		self.available_markets: list = album_dict.get('available_markets')
		self.copyrights: list = album_dict.get('copyrights')
		self.external_ids: dict = album_dict.get('external_ids')
		self.external_urls: dict = album_dict.get('external_urls')
		self.genres: list = album_dict.get('genres')
		self.href: str = album_dict.get('href')
		self.id: str = album_dict.get('id')
		self.images:list = album_dict.get('images', [])
		self.label: str = album_dict.get('label')
		self.name: str = album_dict.get('name')
		self.popularity: int = album_dict.get('popularity')
		self.release_date: str = album_dict.get('release_date')
		self.release_date_precision: str = album_dict.get('release_date_precision')
		self.total_tracks: int = album_dict.get('total_tracks')
		self.tracks: list[Track.Track] = [Track.Track(track) for track in album_dict.get('tracks', {}).get('items', [])]
		self.uri: str = album_dict.get('uri')


	def __str__(self) -> str:
		return self.name

	def getTracks(self):
		return self.tracks