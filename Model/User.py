
class User:

	def __init__(self, userDict) -> None:
		self.display_name: str = userDict.get('display_name')
		self.external_urls: dict = userDict.get('external_urls', {})
		self.followers: dict = userDict.get('followers', {})
		self.href: str = userDict.get('href')
		self.id: str = userDict.get('id')
		self.images: list = userDict.get('images', [])
		self.uri: str = userDict.get('uri')
		self.followers: dict = userDict.get('followers', {})

	def __str__(self) -> str:
		return self.display_name